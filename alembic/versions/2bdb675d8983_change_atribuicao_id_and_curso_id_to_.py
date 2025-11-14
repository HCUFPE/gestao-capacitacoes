"""change_atribuicao_id_and_curso_id_to_string

Revision ID: 2bdb675d8983
Revises: 7668b8cb0e9f
Create Date: 2025-11-13 16:07:38.956724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bdb675d8983'
down_revision: Union[str, Sequence[str], None] = '7668b8cb0e9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('curso_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.alter_column('curso_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
