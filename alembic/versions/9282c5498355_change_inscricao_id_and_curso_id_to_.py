"""change_inscricao_id_and_curso_id_to_string

Revision ID: 9282c5498355
Revises: f84980d72599
Create Date: 2025-11-13 16:42:09.609945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9282c5498355'
down_revision: Union[str, Sequence[str], None] = 'f84980d72599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('inscricoes', schema=None) as batch_op:
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
    with op.batch_alter_table('inscricoes', schema=None) as batch_op:
        batch_op.alter_column('curso_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
