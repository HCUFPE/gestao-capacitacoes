import pytest
from uuid import uuid4
from src.controllers.inscricao_controller import (
    inscrever_usuario_em_curso,
    desinscrever_usuario_de_curso,
)
from src.models import Usuario, Curso, StatusAtribuicao, Atribuicao, Inscricao

@pytest.mark.asyncio
async def test_desinscrever_usuario_em_andamento_sucesso(db_session, test_user_data, test_curso_data):
    user = Usuario(**test_user_data)
    curso = Curso(**test_curso_data)
    db_session.add(user)
    db_session.add(curso)
    await db_session.commit()

    inscricao, atribuicao = await inscrever_usuario_em_curso(db_session, user.id, curso.id)
    assert atribuicao.status == StatusAtribuicao.EM_ANDAMENTO

    success = await desinscrever_usuario_de_curso(db_session, inscricao.id)
    assert success is True

@pytest.mark.asyncio
async def test_desinscrever_usuario_com_certificado_bloqueado(db_session, test_user_data, test_curso_data):
    user = Usuario(**test_user_data)
    curso = Curso(**test_curso_data)
    db_session.add(user)
    db_session.add(curso)
    await db_session.commit()

    inscricao, atribuicao = await inscrever_usuario_em_curso(db_session, user.id, curso.id)
    
    # Simula envio de certificado
    atribuicao.certificado_id = "cert-123"
    atribuicao.status = StatusAtribuicao.REALIZADO
    await db_session.commit()

    with pytest.raises(ValueError, match="Não é possível cancelar uma inscrição que já possui certificado enviado."):
        await desinscrever_usuario_de_curso(db_session, inscricao.id)
