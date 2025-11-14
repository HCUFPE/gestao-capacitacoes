"""change_curso_id_to_string

Revision ID: d0fceefce915
Revises: 96f1ed75e1ad
Create Date: 2025-11-13 15:00:02.906585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0fceefce915'
down_revision: Union[str, Sequence[str], None] = '96f1ed75e1ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
