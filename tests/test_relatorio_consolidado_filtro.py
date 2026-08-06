"""Tests for UDP consolidated report sector filtering."""
import os
import jwt
import pytest
from uuid import uuid4

from src.models import Usuario, Curso, Atribuicao, StatusAtribuicao
from src.models.usuario import PerfilUsuario
from src.controllers import relatorio_controller

JWT_SECRET = os.getenv("JWT_SECRET", "test-secret-key-for-testing")


def _create_token(sub: str, perfil: str) -> str:
    return jwt.encode(
        {"sub": sub, "perfil": perfil},
        JWT_SECRET,
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_get_consolidado_udp_com_filtro_lotacao(db_session):
    """get_relatorio_consolidado should filter results when lotacao param is provided."""
    user1 = Usuario(
        id=str(uuid4()),
        nome="Servidor Setor A",
        perfil=PerfilUsuario.TRABALHADOR,
        lotacao="SETOR A"
    )
    user2 = Usuario(
        id=str(uuid4()),
        nome="Servidor Setor B",
        perfil=PerfilUsuario.TRABALHADOR,
        lotacao="SETOR B"
    )
    curso = Curso(id=str(uuid4()), titulo="Curso Teste", carga_horaria=20)
    
    db_session.add_all([user1, user2, curso])
    await db_session.flush()

    atrib1 = Atribuicao(id=str(uuid4()), user_id=user1.id, curso_id=curso.id, status=StatusAtribuicao.EM_ANDAMENTO)
    atrib2 = Atribuicao(id=str(uuid4()), user_id=user2.id, curso_id=curso.id, status=StatusAtribuicao.EM_ANDAMENTO)
    db_session.add_all([atrib1, atrib2])
    await db_session.commit()

    # Query without lotacao
    all_data = await relatorio_controller.get_relatorio_consolidado(db_session, lotacao=None)
    assert len(all_data) >= 2

    # Query with lotacao=SETOR A
    data_a = await relatorio_controller.get_relatorio_consolidado(db_session, lotacao="SETOR A")
    assert len(data_a) == 1
    assert data_a[0]["setor"] == "SETOR A"


@pytest.mark.asyncio
async def test_export_consolidado_excel_udp_endpoint(async_client, db_session):
    """Excel export endpoint should return status 200 and binary xlsx file without error."""
    token = _create_token("admin.user", PerfilUsuario.UDP.value)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/api/relatorios/udp/consolidado/export/excel", headers=headers)
    assert response.status_code == 200
    assert "spreadsheetml" in response.headers.get("content-type", "")
