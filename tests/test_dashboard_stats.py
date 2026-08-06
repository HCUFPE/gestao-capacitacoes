"""Tests for dashboard stats endpoint."""
import os
import jwt
import pytest
from uuid import uuid4

from src.models import Usuario, Curso, Atribuicao, StatusAtribuicao, Inscricao
from src.models.usuario import PerfilUsuario

from src.auth.auth import auth_handler


def _create_token(sub: str, perfil: str) -> str:
    return auth_handler.create_access_token({"sub": sub, "perfil": perfil})


@pytest.mark.asyncio
async def test_get_dashboard_stats_endpoint(async_client, app):
    """Stats endpoint should return both global and personal stats."""
    db_manager = app.state.app_db
    async with db_manager.async_session_maker() as session:
        user = Usuario(
            id=str(uuid4()),
            nome="Usuario Teste Stats",
            perfil=PerfilUsuario.TRABALHADOR,
            lotacao="SETOR TESTE"
        )
        curso = Curso(id=str(uuid4()), titulo="Curso Stats Teste", carga_horaria=10)
        session.add_all([user, curso])
        await session.flush()

        inscricao = Inscricao(id=str(uuid4()), user_id=user.id, curso_id=curso.id)
        atribuicao = Atribuicao(id=str(uuid4()), user_id=user.id, curso_id=curso.id, status=StatusAtribuicao.VALIDADO)
        session.add_all([inscricao, atribuicao])
        await session.commit()
        user_id = user.id
        perfil = user.perfil.value

    token = _create_token(user_id, perfil)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/api/utils/stats", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_cursos" in data
    assert "total_inscricoes" in data
    assert "total_certificados_validados" in data
    assert "total_usuarios" in data
    assert "minhas_inscricoes" in data
    assert "meus_certificados_enviados" in data
    assert "meus_certificados_validados" in data
    assert data["minhas_inscricoes"] >= 1
