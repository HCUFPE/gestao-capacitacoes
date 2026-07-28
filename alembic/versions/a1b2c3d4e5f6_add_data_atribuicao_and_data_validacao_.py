"""add data_atribuicao and data_validacao to atribuicao, fix enum status values

Revision ID: a1b2c3d4e5f6
Revises: f731a871de84
Create Date: 2026-06-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f731a871de84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new datetime columns
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_atribuicao', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('data_validacao', sa.DateTime(), nullable=True))

    # Fix enum value: "REALIZADO" -> "Realizado"
    op.execute("UPDATE atribuicoes SET status='Realizado' WHERE status='REALIZADO'")


def downgrade() -> None:
    """Downgrade schema."""
    # Revert enum value
    op.execute("UPDATE atribuicoes SET status='REALIZADO' WHERE status='Realizado'")

    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.drop_column('data_validacao')
        batch_op.drop_column('data_atribuicao')
