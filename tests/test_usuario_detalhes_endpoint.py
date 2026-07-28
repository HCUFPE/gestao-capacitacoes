"""Tests for the usuario detalhes endpoint (GET /api/relatorios/usuario/{user_id}/detalhes)."""
import os
import jwt
import pytest
from uuid import uuid4

from src.models import Atribuicao, StatusAtribuicao, Usuario, Curso, Certificado
from src.controllers import relatorio_controller
from src.models.usuario import PerfilUsuario


# JWT secret from environment (same as auth.py)
JWT_SECRET = os.getenv("JWT_SECRET", "test-secret-key-for-testing")


def _create_token(sub: str, perfil: str) -> str:
    """Create a JWT token with the given sub and perfil."""
    return jwt.encode(
        {"sub": sub, "perfil": perfil},
        JWT_SECRET,
        algorithm="HS256",
    )


# --- Task 2.1: UDP acessa detalhes de qualquer usuário (controller) ---

@pytest.mark.asyncio
async def test_get_usuario_detalhes_com_dados(db_session, test_user_data):
    """Controller should return user's assignments with course and certificate details."""
    user = Usuario(
        id=test_user_data["id"],
        nome=test_user_data["nome"],
        lotacao=test_user_data["lotacao"],
    )
    db_session.add(user)
    await db_session.commit()

    curso_id = str(uuid4())
    curso = Curso(id=curso_id, titulo="Curso Teste", ano_gd="2025", certificadora="Corp X", carga_horaria=30)
    db_session.add(curso)
    await db_session.commit()

    atrib_id = str(uuid4())
    atribuicao = Atribuicao(
        id=atrib_id,
        user_id=test_user_data["id"],
        curso_id=curso_id,
        status=StatusAtribuicao.VALIDADO,
    )
    db_session.add(atribuicao)
    await db_session.commit()

    result = await relatorio_controller.get_usuario_detalhes(db_session, test_user_data["id"])
    assert len(result) == 1
    assert result[0]["curso"]["titulo"] == "Curso Teste"
    assert result[0]["status"] == "Validado"
    assert result[0]["user_id"] == test_user_data["id"]
    assert result[0]["curso"]["carga_horaria"] == 30


# --- Task 2.2: Chefia acessa subordinado da mesma lotação (controller permission) ---

@pytest.mark.asyncio
async def test_can_access_chefia_mesma_lotacao(db_session):
    """Chefia should access users in the same lotação."""
    chefia_user = Usuario(
        id="chefia-1",
        nome="Chefia Teste",
        perfil=PerfilUsuario.CHEFIA,
        lotacao="LOTAÇÃO-A",
    )
    sub = Usuario(
        id="sub-1",
        nome="Subordinado",
        perfil=PerfilUsuario.TRABALHADOR,
        lotacao="LOTAÇÃO-A",
    )
    db_session.add(chefia_user)
    db_session.add(sub)
    await db_session.commit()

    current_user = {"sub": "chefia-1", "perfil": PerfilUsuario.CHEFIA.value}
    # Should not raise
    await relatorio_controller.can_access_user_details(db_session, current_user, "sub-1")


# --- Task 2.3: Chefia não acessa usuário de outra lotação (403) ---

@pytest.mark.asyncio
async def test_can_access_chefia_outra_lotacao_403(db_session):
    """Chefia should NOT access users from a different lotação (403)."""
    chefia_user = Usuario(
        id="chefia-2",
        nome="Chefia Teste 2",
        perfil=PerfilUsuario.CHEFIA,
        lotacao="LOTAÇÃO-A",
    )
    target = Usuario(
        id="target-2",
        nome="Outro Usuário",
        perfil=PerfilUsuario.TRABALHADOR,
        lotacao="LOTAÇÃO-B",
    )
    db_session.add(chefia_user)
    db_session.add(target)
    await db_session.commit()

    current_user = {"sub": "chefia-2", "perfil": PerfilUsuario.CHEFIA.value}

    with pytest.raises(Exception) as exc:
        await relatorio_controller.can_access_user_details(db_session, current_user, "target-2")
    assert "403" in str(exc.value) or "403" in str(exc.value.__cause__) or exc.value.status_code == 403


# --- Task 2.4: Trabalhador não acessa detalhes (403) ---

@pytest.mark.asyncio
async def test_can_access_trabalhador_403(db_session):
    """Trabalhador should NOT access any user details (403)."""
    current_user = {"sub": "trab-1", "perfil": PerfilUsuario.TRABALHADOR.value}

    with pytest.raises(Exception) as exc:
        await relatorio_controller.can_access_user_details(db_session, current_user, "any-user")
    assert exc.value.status_code == 403


# --- Task 2.5: Usuário não encontrado (404) ---

@pytest.mark.asyncio
async def test_can_access_usuario_nao_encontrado_404(db_session):
    """Requesting details for a non-existent user should return 404."""
    udp_user = {"sub": "udp-1", "perfil": PerfilUsuario.UDP.value}

    with pytest.raises(Exception) as exc:
        await relatorio_controller.can_access_user_details(db_session, udp_user, "non-existent")
    assert exc.value.status_code == 404


# --- Task 2.6: UDP acessa qualquer usuário (sem restrição) ---

@pytest.mark.asyncio
async def test_can_access_udp_any_user(db_session):
    """UDP should access any user without restrictions."""
    target = Usuario(
        id="target-udp",
        nome="Alvo UDP",
        perfil=PerfilUsuario.TRABALHADOR,
        lotacao="QUALQUER",
    )
    db_session.add(target)
    await db_session.commit()

    udp_user = {"sub": "udp-user", "perfil": PerfilUsuario.UDP.value}
    # Should not raise
    await relatorio_controller.can_access_user_details(db_session, udp_user, "target-udp")


# --- Additional: user with no assignments returns empty list ---

@pytest.mark.asyncio
async def test_get_usuario_detalhes_sem_atribuicoes(db_session):
    """Controller should return empty list for user with no assignments."""
    result = await relatorio_controller.get_usuario_detalhes(db_session, "user-sem-atribuicoes")
    assert result == []


# --- HTTP Integration Tests ---

@pytest.mark.asyncio
async def test_endpoint_udp_acessa_detalhes(async_client, db_session):
    """UDP should be able to access details of any user via HTTP."""
    # Insert data into the DB used by the app
    from src.main import app
    db_manager = app.state.app_db
    async with db_manager.async_session_maker() as session:
        target_id = str(uuid4())
        user = Usuario(
            id=target_id,
            nome="Usuário Alvo",
            perfil=PerfilUsuario.TRABALHADOR,
            lotacao="LOTAÇÃO-X",
        )
        curso = Curso(id=str(uuid4()), titulo="Curso HTTP", ano_gd="2025", certificadora="Corp Y", carga_horaria=15)
        atribuicao = Atribuicao(
            id=str(uuid4()),
            user_id=target_id,
            curso_id=curso.id,
            status=StatusAtribuicao.REALIZADO,
        )
        session.add(user)
        session.add(curso)
        session.add(atribuicao)
        await session.commit()

    udp_token = _create_token("udp-test", PerfilUsuario.UDP.value)
    response = await async_client.get(
        f"/api/relatorios/usuario/{target_id}/detalhes",
        headers={"Authorization": f"Bearer {udp_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["curso"]["titulo"] == "Curso HTTP"


@pytest.mark.asyncio
async def test_endpoint_trabalhador_403(async_client):
    """Trabalhador should be blocked from the endpoint (403)."""
    trabalhador_token = _create_token("trab-test", PerfilUsuario.TRABALHADOR.value)
    response = await async_client.get(
        "/api/relatorios/usuario/some-user-id/detalhes",
        headers={"Authorization": f"Bearer {trabalhador_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_endpoint_chefia_403_outra_lotacao(async_client, db_session):
    """Chefia should be blocked when accessing user from different lotação (403)."""
    from src.main import app
    db_manager = app.state.app_db
    async with db_manager.async_session_maker() as session:
        chefia_user = Usuario(
            id="chefia-http",
            nome="Chefia HTTP",
            perfil=PerfilUsuario.CHEFIA,
            lotacao="LOTAÇÃO-ALPHA",
        )
        target = Usuario(
            id="target-http",
            nome="Alvo HTTP",
            perfil=PerfilUsuario.TRABALHADOR,
            lotacao="LOTAÇÃO-BETA",
        )
        session.add(chefia_user)
        session.add(target)
        await session.commit()

    chefia_token = _create_token("chefia-http", PerfilUsuario.CHEFIA.value)
    response = await async_client.get(
        "/api/relatorios/usuario/target-http/detalhes",
        headers={"Authorization": f"Bearer {chefia_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_endpoint_usuario_nao_encontrado(async_client):
    """Non-existent user should return 404."""
    udp_token = _create_token("udp-test2", PerfilUsuario.UDP.value)
    response = await async_client.get(
        "/api/relatorios/usuario/non-existent-user/detalhes",
        headers={"Authorization": f"Bearer {udp_token}"},
    )
    assert response.status_code == 404
