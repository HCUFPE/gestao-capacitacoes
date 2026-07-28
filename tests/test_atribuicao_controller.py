"""Tests for the atribuicao controller."""
import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import select

from src.models import Atribuicao, StatusAtribuicao, Usuario, Curso, Certificado
from src.controllers import atribuicao_controller


@pytest.mark.asyncio
async def test_criar_atribuicoes_para_lotacao(db_session, test_user_data):
    """Creating assignments should insert records with PENDENTE status."""
    user = Usuario(
        id=test_user_data["id"],
        nome=test_user_data["nome"],
        lotacao=test_user_data["lotacao"],
        matricula=test_user_data["matricula"],
    )
    db_session.add(user)
    await db_session.commit()

    curso_id = str(uuid4())
    curso = Curso(id=curso_id, titulo="Curso X", ano_gd="2025")
    db_session.add(curso)
    await db_session.commit()

    await atribuicao_controller.criar_atribuicoes_para_lotacao(
        db_session, curso_id, test_user_data["lotacao"]
    )

    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.curso_id == curso_id)
    )
    atribuicoes = result.scalars().all()
    assert len(atribuicoes) == 1
    assert atribuicoes[0].status == StatusAtribuicao.PENDENTE


@pytest.mark.asyncio
async def test_criar_atribuicoes_lotacao_vazia(db_session):
    """Creating assignments for an empty lotação should produce no records."""
    await atribuicao_controller.criar_atribuicoes_para_lotacao(
        db_session, str(uuid4()), "lotacao-inexistente"
    )
    result = await db_session.execute(select(Atribuicao))
    assert result.scalars().all() == []


@pytest.mark.asyncio
async def test_atualizar_atribuicao_com_certificado(db_session, test_user_data):
    """Updating attribution with certificate should set status and data_conclusao."""
    user = Usuario(
        id=test_user_data["id"],
        nome=test_user_data["nome"],
        lotacao=test_user_data["lotacao"],
    )
    db_session.add(user)
    await db_session.commit()

    atribuicao_id = str(uuid4())
    curso_id = str(uuid4())
    cert_id = str(uuid4())

    atrib = Atribuicao(
        id=atribuicao_id,
        user_id=user.id,
        curso_id=curso_id,
        status=StatusAtribuicao.EM_ANDAMENTO,
    )
    db_session.add(atrib)
    await db_session.commit()

    await atribuicao_controller.atualizar_atribuicao_com_certificado(
        db_session, atribuicao_id, cert_id, StatusAtribuicao.REALIZADO
    )

    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.id == atribuicao_id)
    )
    atrib = result.scalar_one()
    assert atrib.status == StatusAtribuicao.REALIZADO
    assert atrib.certificado_id == cert_id
    assert atrib.data_conclusao is not None


@pytest.mark.asyncio
async def test_validar_atribuicao(db_session):
    """Validating attribution should update status and set data_validacao."""
    atribuicao_id = str(uuid4())
    atrib = Atribuicao(
        id=atribuicao_id,
        user_id="u-teste",
        curso_id=str(uuid4()),
        status=StatusAtribuicao.REALIZADO,
    )
    db_session.add(atrib)
    await db_session.commit()

    await atribuicao_controller.validar_atribuicao(
        db_session, atribuicao_id, StatusAtribuicao.VALIDADO
    )

    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.id == atribuicao_id)
    )
    atrib = result.scalar_one()
    assert atrib.status == StatusAtribuicao.VALIDADO
    assert atrib.data_validacao is not None


@pytest.mark.asyncio
async def test_validar_atribuicao_recusado(db_session):
    """Rejecting attribution should set status to RECUSADO."""
    atribuicao_id = str(uuid4())
    atrib = Atribuicao(
        id=atribuicao_id,
        user_id="u-teste",
        curso_id=str(uuid4()),
        status=StatusAtribuicao.REALIZADO,
    )
    db_session.add(atrib)
    await db_session.commit()

    await atribuicao_controller.validar_atribuicao(
        db_session, atribuicao_id, StatusAtribuicao.RECUSADO
    )

    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.id == atribuicao_id)
    )
    atrib = result.scalar_one()
    assert atrib.status == StatusAtribuicao.RECUSADO


@pytest.mark.asyncio
async def test_listar_atribuicoes_por_usuario(db_session, test_curso_data):
    """Listing user attributions should return certificate data in response."""
    curso = Curso(**test_curso_data)
    db_session.add(curso)
    await db_session.commit()

    cert = Certificado(id="cert-1", curso_id=curso.id, file_path="/uploads/cert.pdf", link="https://example.com/cert")
    db_session.add(cert)
    await db_session.commit()

    atrib = Atribuicao(
        id=str(uuid4()),
        user_id="u-teste",
        curso_id=curso.id,
        status=StatusAtribuicao.REALIZADO,
        certificado_id=cert.id,
    )
    db_session.add(atrib)
    await db_session.commit()

    resultado = await atribuicao_controller.listar_atribuicoes_por_usuario(
        db_session, "u-teste"
    )

    assert len(resultado) == 1
    item = resultado[0]
    assert item["certificado_id"] == cert.id
    assert item["certificado_file_path"] == cert.file_path
    assert item["certificado_link"] == cert.link
    assert item["curso"]["titulo"] == curso.titulo


@pytest.mark.asyncio
async def test_listar_atribuicoes_sem_certificado(db_session, test_curso_data):
    """Listing attribution without certificate should return None for cert fields."""
    curso = Curso(**test_curso_data)
    db_session.add(curso)
    await db_session.commit()

    atrib = Atribuicao(
        id=str(uuid4()),
        user_id="u-teste",
        curso_id=curso.id,
        status=StatusAtribuicao.PENDENTE,
    )
    db_session.add(atrib)
    await db_session.commit()

    resultado = await atribuicao_controller.listar_atribuicoes_por_usuario(
        db_session, "u-teste"
    )

    assert len(resultado) == 1
    assert resultado[0]["certificado_id"] is None
    assert resultado[0]["certificado_file_path"] is None
    assert resultado[0]["certificado_link"] is None


@pytest.mark.asyncio
async def test_listar_atribuicoes_pendentes_validacao(db_session):
    """Should return only REALIZADO attributions for the given lotação."""
    user1 = Usuario(id="u1", nome="User1", lotacao="lot-a")
    user2 = Usuario(id="u2", nome="User2", lotacao="lot-a")
    user3 = Usuario(id="u3", nome="User3", lotacao="lot-b")
    db_session.add_all([user1, user2, user3])
    await db_session.commit()

    curso = Curso(id=str(uuid4()), titulo="Curso Pendente", ano_gd="2025")
    db_session.add(curso)
    await db_session.commit()

    db_session.add_all([
        Atribuicao(id=str(uuid4()), user_id="u1", curso_id=curso.id, status=StatusAtribuicao.REALIZADO, data_conclusao=datetime.utcnow()),
        Atribuicao(id=str(uuid4()), user_id="u2", curso_id=curso.id, status=StatusAtribuicao.PENDENTE),
        Atribuicao(id=str(uuid4()), user_id="u3", curso_id=curso.id, status=StatusAtribuicao.REALIZADO, data_conclusao=datetime.utcnow()),
    ])
    await db_session.commit()

    resultado = await atribuicao_controller.listar_atribuicoes_pendentes_validacao(
        db_session, "lot-a"
    )

    assert len(resultado) == 1  # only u1's REALIZADO in lot-a
    assert resultado[0]["usuario_nome"] == "User1"
