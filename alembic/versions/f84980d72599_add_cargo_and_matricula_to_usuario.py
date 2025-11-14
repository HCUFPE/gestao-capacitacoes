"""add_cargo_and_matricula_to_usuario

Revision ID: f84980d72599
Revises: 2bdb675d8983
Create Date: 2025-11-13 16:35:04.430843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f84980d72599'
down_revision: Union[str, Sequence[str], None] = '2bdb675d8983'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cargo', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('matricula', sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('matricula')
        batch_op.drop_column('cargo')
