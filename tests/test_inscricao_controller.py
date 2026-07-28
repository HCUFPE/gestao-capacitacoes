"""Tests for the inscricao controller."""
import pytest
from uuid import uuid4
from sqlalchemy import select

from src.models import Inscricao, Atribuicao, StatusAtribuicao, Usuario, Curso, Certificado
from src.controllers import inscricao_controller


@pytest.mark.asyncio
async def test_listar_inscricoes_por_usuario(db_session):
    """Should return inscricoes with curso data and certificate fields for the given user."""
    user = Usuario(id="u1", nome="Teste", lotacao="lot")
    curso = Curso(id=str(uuid4()), titulo="Curso Inscricao", ano_gd="2025")
    db_session.add_all([user, curso])
    await db_session.commit()

    inscricao = Inscricao(
        id=str(uuid4()),
        user_id="u1",
        curso_id=curso.id,
    )
    # Atribuicao is required for listar_inscricoes_por_usuario (JOIN)
    atrib = Atribuicao(
        id=str(uuid4()),
        user_id="u1",
        curso_id=curso.id,
        status=StatusAtribuicao.EM_ANDAMENTO,
    )
    db_session.add_all([inscricao, atrib])
    await db_session.commit()

    resultado = await inscricao_controller.listar_inscricoes_por_usuario(db_session, "u1")
    assert len(resultado) == 1
    assert resultado[0]["curso"]["titulo"] == "Curso Inscricao"
    assert resultado[0]["certificado_id"] is None
    assert resultado[0]["certificado_file_path"] is None
    assert resultado[0]["certificado_link"] is None


@pytest.mark.asyncio
async def test_listar_inscricoes_com_certificado(db_session):
    """Should return certificate data when certificado is linked."""
    user = Usuario(id="u2", nome="Teste2", lotacao="lot")
    curso = Curso(id=str(uuid4()), titulo="Curso Cert", ano_gd="2025")
    cert = Certificado(id="cert-1", curso_id=curso.id, file_path="/uploads/c.pdf", link="https://example.com/c")
    db_session.add_all([user, curso, cert])
    await db_session.commit()

    inscricao = Inscricao(id=str(uuid4()), user_id="u2", curso_id=curso.id)
    atrib = Atribuicao(
        id=str(uuid4()),
        user_id="u2",
        curso_id=curso.id,
        status=StatusAtribuicao.REALIZADO,
        certificado_id=cert.id,
    )
    db_session.add_all([inscricao, atrib])
    await db_session.commit()

    resultado = await inscricao_controller.listar_inscricoes_por_usuario(db_session, "u2")
    assert len(resultado) == 1
    assert resultado[0]["certificado_id"] == "cert-1"
    assert resultado[0]["certificado_file_path"] == "/uploads/c.pdf"
    assert resultado[0]["certificado_link"] == "https://example.com/c"


@pytest.mark.asyncio
async def test_listar_inscricoes_usuario_sem_inscricao(db_session):
    """Should return empty list for user with no inscricoes."""
    resultado = await inscricao_controller.listar_inscricoes_por_usuario(db_session, "nao-existe")
    assert resultado == []


@pytest.mark.asyncio
async def test_inscriar_usuario_em_curso(db_session):
    """Should create inscricao and atribuicao with EM_ANDAMENTO status."""
    user = Usuario(id="u3", nome="Teste3", lotacao="lot")
    curso = Curso(id=str(uuid4()), titulo="Curso Novo", ano_gd="2025")
    db_session.add_all([user, curso])
    await db_session.commit()

    inscricao, atrib = await inscricao_controller.inscrever_usuario_em_curso(
        db_session, "u3", curso.id
    )

    assert inscricao.user_id == "u3"
    assert inscricao.curso_id == curso.id
    assert atrib.status == StatusAtribuicao.EM_ANDAMENTO
    assert atrib.criado_por_usuario is True


@pytest.mark.asyncio
async def test_desinscrever_usuario_de_curso(db_session):
    """Should remove inscricao and delete user-created atribuicao."""
    user = Usuario(id="u4", nome="Teste4", lotacao="lot")
    curso = Curso(id=str(uuid4()), titulo="Curso Remover", ano_gd="2025")
    db_session.add_all([user, curso])
    await db_session.commit()

    inscricao, atrib = await inscricao_controller.inscrever_usuario_em_curso(
        db_session, "u4", curso.id
    )

    result = await inscricao_controller.desinscrever_usuario_de_curso(
        db_session, inscricao.id
    )
    assert result is True

    # Inscricao should be gone
    check = await db_session.execute(select(Inscricao).where(Inscricao.id == inscricao.id))
    assert check.scalar_one_or_none() is None

    # Atribuicao created by user should be deleted
    check_attr = await db_session.execute(
        select(Atribuicao).where(Atribuicao.user_id == "u4", Atribuicao.curso_id == curso.id)
    )
    assert check_attr.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_desinscrever_usuario_curso_nao_encontrado(db_session):
    """Should return False for non-existent inscricao."""
    result = await inscricao_controller.desinscrever_usuario_de_curso(
        db_session, "inexistente"
    )
    assert result is False
