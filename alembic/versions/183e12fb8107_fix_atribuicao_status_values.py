"""fix_atribuicao_status_values

Revision ID: 183e12fb8107
Revises: a1b2c3d4e5f6
Create Date: 2026-08-05 16:58:58.580263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '183e12fb8107'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE atribuicoes SET status = 'PENDENTE' WHERE status = 'Pendente';")
    op.execute("UPDATE atribuicoes SET status = 'EM_ANDAMENTO' WHERE status = 'Em Andamento';")
    op.execute("UPDATE atribuicoes SET status = 'REALIZADO' WHERE status = 'Realizado';")
    op.execute("UPDATE atribuicoes SET status = 'VALIDADO' WHERE status = 'Validado';")
    op.execute("UPDATE atribuicoes SET status = 'RECUSADO' WHERE status = 'Recusado';")
    op.execute("UPDATE atribuicoes SET status = 'CONCLUIDO' WHERE status = 'Concluído';")

def downgrade() -> None:
    """Downgrade schema."""
    pass
