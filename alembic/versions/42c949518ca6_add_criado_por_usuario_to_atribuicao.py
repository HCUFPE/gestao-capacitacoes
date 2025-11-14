"""add criado_por_usuario to atribuicao

Revision ID: 42c949518ca6
Revises: 9282c5498355
Create Date: 2025-11-13 17:43:13.132871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42c949518ca6'
down_revision: Union[str, Sequence[str], None] = '9282c5498355'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('criado_por_usuario', sa.Boolean(), nullable=False, server_default=sa.text("'0'")))
        batch_op.alter_column('status',
                   existing_type=sa.VARCHAR(length=9),
                   type_=sa.Enum('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDO', 'REALIZADO', name='statusatribuicao'),
                   nullable=True)

    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column('atribuir_a_todos',
                   existing_type=sa.BOOLEAN(),
                   nullable=True,
                   existing_server_default=sa.text("'0'"))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column('atribuir_a_todos',
                   existing_type=sa.BOOLEAN(),
                   nullable=False,
                   existing_server_default=sa.text("'0'"))

    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.alter_column('status',
                   existing_type=sa.Enum('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDO', 'REALIZADO', name='statusatribuicao'),
                   type_=sa.VARCHAR(length=9),
                   nullable=False)
        batch_op.drop_column('criado_por_usuario')
