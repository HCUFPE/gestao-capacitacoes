"""add certificado_id and data_conclusao to atribuicao

Revision ID: 85d79b471ed2
Revises: f6a3ad128da8
Create Date: 2025-11-13 18:48:33.212618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85d79b471ed2'
down_revision: Union[str, Sequence[str], None] = 'f6a3ad128da8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('certificado_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('data_conclusao', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key('fk_atribuicoes_certificado_id', 'certificados', ['certificado_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_atribuicoes_certificado_id', type_='foreignkey')
        batch_op.drop_column('data_conclusao')
        batch_op.drop_column('certificado_id')
