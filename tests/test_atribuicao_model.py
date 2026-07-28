"""Tests for the StatusAtribuicao enum and Atribuicao model."""
import pytest
from src.models.atribuicao import StatusAtribuicao, Atribuicao


class TestStatusAtribuicao:
    def test_pendente_value(self):
        assert StatusAtribuicao.PENDENTE.value == "Pendente"

    def test_em_andamento_value(self):
        assert StatusAtribuicao.EM_ANDAMENTO.value == "Em Andamento"

    def test_realizado_title_case(self):
        assert StatusAtribuicao.REALIZADO.value == "Realizado"

    def test_validado_exists(self):
        assert StatusAtribuicao.VALIDADO.value == "Validado"

    def test_recusado_exists(self):
        assert StatusAtribuicao.RECUSADO.value == "Recusado"

    def test_concluido_exists(self):
        assert StatusAtribuicao.CONCLUIDO.value == "Concluído"

    def test_all_values_title_case(self):
        """All enum values should use Title Case for consistency."""
        for member in StatusAtribuicao:
            val = member.value
            assert val[0].isupper(), f"{member.name}='{val}' should start with uppercase"

    def test_enum_from_string(self):
        assert StatusAtribuicao("Realizado") == StatusAtribuicao.REALIZADO

    def test_enum_members_count(self):
        expected = {"PENDENTE", "EM_ANDAMENTO", "REALIZADO", "VALIDADO", "RECUSADO", "CONCLUIDO"}
        actual = {member.name for member in StatusAtribuicao}
        assert actual == expected


class TestAtribuicaoModel:
    def test_repr(self):
        attr = Atribuicao(
            id="123",
            user_id="u1",
            curso_id="c1",
            status=StatusAtribuicao.PENDENTE,
        )
        assert "123" in repr(attr)
        assert "u1" in repr(attr)
        assert "Pendente" in repr(attr)

    def test_default_status(self):
        """Column default applies at DB level; constructor leaves it None."""
        attr = Atribuicao(
            id="123",
            user_id="u1",
            curso_id="c1",
        )
        assert attr.status is None  # Column default is DB-side, not Python-side
