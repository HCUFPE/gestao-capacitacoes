"""Tests for granular (seletiva) course assignment."""
import pytest
from uuid import uuid4
from sqlalchemy import select

from src.models import Atribuicao, StatusAtribuicao, Usuario, Curso
from src.controllers import atribuicao_controller


@pytest.fixture
def chefia_user_data():
    """Sample chefia user data."""
    return {
        "id": "chefia-001",
        "nome": "Chefe Teste",
        "perfil": "CHEFIA",
        "lotacao": "lotacao-chefia",
        "matricula": "999999",
        "cargo": "Chefe",
    }


@pytest.fixture
def subordinados_data(chefia_user_data):
    """Three subordinate users in the chefia's lotacao."""
    return [
        {
            "id": "sub-001",
            "nome": "Subordinado 1",
            "perfil": "TRABALHADOR",
            "lotacao": chefia_user_data["lotacao"],
            "matricula": "111111",
        },
        {
            "id": "sub-002",
            "nome": "Subordinado 2",
            "perfil": "TRABALHADOR",
            "lotacao": chefia_user_data["lotacao"],
            "matricula": "222222",
        },
        {
            "id": "sub-003",
            "nome": "Subordinado 3",
            "perfil": "TRABALHADOR",
            "lotacao": chefia_user_data["lotacao"],
            "matricula": "333333",
        },
    ]


@pytest.fixture
def outro_setor_user_data():
    """A user from a different lotacao."""
    return {
        "id": "outro-001",
        "nome": "Outro Setor",
        "perfil": "TRABALHADOR",
        "lotacao": "outra-lotacao",
        "matricula": "444444",
    }


@pytest.mark.asyncio
async def test_criar_atribuicoes_seletivas_3_usuarios(
    db_session, subordinados_data, chefia_user_data
):
    """Task 8.1: Chefia selects 3 users -> 3 attributions created.

    WHEN chefia sends a list of 3 valid user_ids from her lotacao
    THEN 3 new Atribuicao records are created with status PENDENTE
    """
    # Arrange: create curso
    curso_id = str(uuid4())
    curso = Curso(id=curso_id, titulo="Curso Seletivo", ano_gd="2025")
    db_session.add(curso)
    await db_session.commit()

    # Arrange: create 3 subordinados
    for u in subordinados_data:
        db_session.add(Usuario(**u))
    await db_session.commit()

    # Act: call seletiva with 3 user_ids
    user_ids = [u["id"] for u in subordinados_data]
    await atribuicao_controller.criar_atribuicoes_seletivas(
        db_session,
        curso_id=curso_id,
        user_ids=user_ids,
        chefia_lotacao=chefia_user_data["lotacao"],
    )

    # Assert: 3 atribuicoes created
    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.curso_id == curso_id)
    )
    atribuicoes = result.scalars().all()
    assert len(atribuicoes) == 3
    for a in atribuicoes:
        assert a.status == StatusAtribuicao.PENDENTE
        assert a.user_id in user_ids


@pytest.mark.asyncio
async def test_criar_atribuicoes_seletivas_usuario_outro_setor_403(
    db_session, subordinados_data, outro_setor_user_data, chefia_user_data
):
    """Task 8.2: Chefia tries to assign user from another lotacao -> ValueError (HTTP 403 in router).

    WHEN chefia includes a user_id from a different lotacao
    THEN system raises ValueError for that user
    """
    # Arrange: create curso
    curso_id = str(uuid4())
    curso = Curso(id=curso_id, titulo="Curso Seletivo 2", ano_gd="2025")
    db_session.add(curso)
    await db_session.commit()

    # Arrange: create subordinados + user from another lotacao
    for u in subordinados_data:
        db_session.add(Usuario(**u))
    db_session.add(Usuario(**outro_setor_user_data))
    await db_session.commit()

    # Act + Assert: include user from other lotacao -> ValueError
    user_ids = [subordinados_data[0]["id"], outro_setor_user_data["id"]]
    with pytest.raises(ValueError, match="não pertence à lotação da chefia"):
        await atribuicao_controller.criar_atribuicoes_seletivas(
            db_session,
            curso_id=curso_id,
            user_ids=user_ids,
            chefia_lotacao=chefia_user_data["lotacao"],
        )

    # Assert: no atribuicoes created for the other lotacao user
    result = await db_session.execute(
        select(Atribuicao).where(
            Atribuicao.curso_id == curso_id,
            Atribuicao.user_id == outro_setor_user_data["id"],
        )
    )
    assert result.scalars().all() == []


@pytest.mark.asyncio
async def test_criar_atribuicoes_seletivas_ignora_duplicatas(
    db_session, subordinados_data, chefia_user_data
):
    """Seletiva assignment should ignore users who already have the course."""
    curso_id = str(uuid4())
    curso = Curso(id=curso_id, titulo="Curso Duplicata", ano_gd="2025")
    db_session.add(curso)
    await db_session.commit()

    for u in subordinados_data:
        db_session.add(Usuario(**u))
    await db_session.commit()

    # Pre-create one atribuicao
    db_session.add(
        Atribuicao(
            id=str(uuid4()),
            user_id=subordinados_data[0]["id"],
            curso_id=curso_id,
            status=StatusAtribuicao.PENDENTE,
        )
    )
    await db_session.commit()

    # Act: call seletiva with all 3 (one already exists)
    user_ids = [u["id"] for u in subordinados_data]
    await atribuicao_controller.criar_atribuicoes_seletivas(
        db_session,
        curso_id=curso_id,
        user_ids=user_ids,
        chefia_lotacao=chefia_user_data["lotacao"],
    )

    # Assert: only 3 total (1 existing + 2 new)
    result = await db_session.execute(
        select(Atribuicao).where(Atribuicao.curso_id == curso_id)
    )
    assert len(result.scalars().all()) == 3
