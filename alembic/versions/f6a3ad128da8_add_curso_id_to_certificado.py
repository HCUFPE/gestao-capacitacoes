"""add curso_id to certificado

Revision ID: f6a3ad128da8
Revises: 42c949518ca6
Create Date: 2025-11-13 18:35:26.796799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6a3ad128da8'
down_revision: Union[str, Sequence[str], None] = '42c949518ca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('certificados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('curso_id', sa.String(), nullable=True)) # Add as nullable first
        batch_op.create_foreign_key('fk_certificados_curso_id', 'cursos', ['curso_id'], ['id']) # Add foreign key

    # If there were existing certificates, you would need to populate curso_id here
    # For now, we assume no existing certificates or they are invalid without a course_id

    with op.batch_alter_table('certificados', schema=None) as batch_op:
        batch_op.alter_column('curso_id',
                   existing_type=sa.String(),
                   nullable=False) # Then make it non-nullable

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('certificados', schema=None) as batch_op:
        batch_op.drop_constraint('fk_certificados_curso_id', type_='foreignkey')
        batch_op.drop_column('curso_id')
