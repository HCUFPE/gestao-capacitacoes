"""Tests for the certificate re-upload/upsert endpoint."""
import pytest
import os
import jwt
from uuid import uuid4
from src.models import Atribuicao, StatusAtribuicao, Usuario, Curso, Certificado
from src.models.usuario import PerfilUsuario

from src.auth.auth import auth_handler

def _create_token(sub: str, perfil: str) -> str:
    """Create a JWT token with the given sub and perfil."""
    return auth_handler.create_access_token({"sub": sub, "perfil": perfil})

@pytest.mark.asyncio
async def test_reupload_certificado_file_success(async_client, app):
    """Should successfully overwrite existing file certificate, delete old file, and change status to REALIZADO."""
    db_manager = app.state.app_db
    uploads_dir = os.path.join("src", "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Pre-create old file on disk
    old_file_name = f"old-{uuid4()}.pdf"
    old_file_path = os.path.join(uploads_dir, old_file_name)
    with open(old_file_path, "wb") as f:
        f.write(b"old-content")

    async with db_manager.async_session_maker() as session:
        user_id = str(uuid4())
        user = Usuario(id=user_id, nome="Usuário Teste", perfil=PerfilUsuario.TRABALHADOR, lotacao="LOTA-X")
        curso = Curso(id=str(uuid4()), titulo="Curso Reupload", ano_gd="2025")
        
        certificado = Certificado(id=str(uuid4()), curso_id=curso.id, file_path=old_file_path, validado=False)
        atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=user_id,
            curso_id=curso.id,
            status=StatusAtribuicao.RECUSADO, # Status is Recusado, allowing reupload
            certificado_id=certificado.id
        )
        
        session.add(user)
        session.add(curso)
        session.add(certificado)
        session.add(atribuicao)
        await session.commit()
        
        atrib_id = atribuicao.id
        cert_id = certificado.id

    token = _create_token(user_id, PerfilUsuario.TRABALHADOR.value)

    # Perform file reupload
    files = {"file": ("new_cert.pdf", b"new-content-pdf", "application/pdf")}
    response = await async_client.post(
        "/api/certificados/upload",
        data={"atribuicao_id": atrib_id},
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["id"] == cert_id
    assert res_data["file_path"] is not None
    assert res_data["file_path"] != old_file_path

    # Old file should be deleted from disk
    assert not os.path.exists(old_file_path)
    
    # Clean up new file
    if os.path.exists(res_data["file_path"]):
        os.remove(res_data["file_path"])

    # DB state assertion
    async with db_manager.async_session_maker() as session:
        from sqlalchemy import select
        res = await session.execute(select(Atribuicao).where(Atribuicao.id == atrib_id))
        updated_atrib = res.scalars().first()
        assert updated_atrib.status == StatusAtribuicao.REALIZADO

@pytest.mark.asyncio
async def test_reupload_certificado_link_success(async_client, app):
    """Should successfully overwrite existing certificate with link, delete old file, and change status to REALIZADO."""
    db_manager = app.state.app_db
    uploads_dir = os.path.join("src", "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Pre-create old file on disk
    old_file_name = f"old-{uuid4()}.pdf"
    old_file_path = os.path.join(uploads_dir, old_file_name)
    with open(old_file_path, "wb") as f:
        f.write(b"old-content")

    async with db_manager.async_session_maker() as session:
        user_id = str(uuid4())
        user = Usuario(id=user_id, nome="Usuário Teste Link", perfil=PerfilUsuario.TRABALHADOR, lotacao="LOTA-X")
        curso = Curso(id=str(uuid4()), titulo="Curso Link Reupload", ano_gd="2025")
        
        certificado = Certificado(id=str(uuid4()), curso_id=curso.id, file_path=old_file_path, validado=False)
        atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=user_id,
            curso_id=curso.id,
            status=StatusAtribuicao.RECUSADO,
            certificado_id=certificado.id
        )
        
        session.add(user)
        session.add(curso)
        session.add(certificado)
        session.add(atribuicao)
        await session.commit()
        
        atrib_id = atribuicao.id
        cert_id = certificado.id

    token = _create_token(user_id, PerfilUsuario.TRABALHADOR.value)

    # Perform link upload
    response = await async_client.post(
        "/api/certificados/link",
        json={"atribuicao_id": atrib_id, "link": "https://new-link.com/cert"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["id"] == cert_id
    assert res_data["link"] == "https://new-link.com/cert"
    assert res_data["file_path"] is None

    # Old file should be deleted from disk
    assert not os.path.exists(old_file_path)

    # DB state assertion
    async with db_manager.async_session_maker() as session:
        from sqlalchemy import select
        res = await session.execute(select(Atribuicao).where(Atribuicao.id == atrib_id))
        updated_atrib = res.scalars().first()
        assert updated_atrib.status == StatusAtribuicao.REALIZADO

@pytest.mark.asyncio
async def test_reupload_certificado_rejected_if_validated_or_concluded(async_client, app):
    """Should reject re-upload if status is VALIDADO or CONCLUIDO."""
    db_manager = app.state.app_db

    async with db_manager.async_session_maker() as session:
        user_id = str(uuid4())
        user = Usuario(id=user_id, nome="Usuário Teste Rejeita", perfil=PerfilUsuario.TRABALHADOR, lotacao="LOTA-X")
        curso = Curso(id=str(uuid4()), titulo="Curso Rejeitado", ano_gd="2025")
        
        certificado = Certificado(id=str(uuid4()), curso_id=curso.id, link="https://old-link.com", validado=True)
        atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=user_id,
            curso_id=curso.id,
            status=StatusAtribuicao.VALIDADO,
            certificado_id=certificado.id
        )
        
        session.add(user)
        session.add(curso)
        session.add(certificado)
        session.add(atribuicao)
        await session.commit()
        
        atrib_id = atribuicao.id

    token = _create_token(user_id, PerfilUsuario.TRABALHADOR.value)

    # Perform upload file (should fail)
    files = {"file": ("new_cert.pdf", b"new-content-pdf", "application/pdf")}
    response = await async_client.post(
        "/api/certificados/upload",
        data={"atribuicao_id": atrib_id},
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "Não é possível alterar" in response.json()["detail"]

    # Perform link update (should fail)
    response2 = await async_client.post(
        "/api/certificados/link",
        json={"atribuicao_id": atrib_id, "link": "https://new-link.com/cert"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 400
    assert "Não é possível alterar" in response2.json()["detail"]
