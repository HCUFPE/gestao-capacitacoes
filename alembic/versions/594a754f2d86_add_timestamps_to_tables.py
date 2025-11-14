"""add_timestamps_to_tables

Revision ID: 594a754f2d86
Revises: b0a58a5187a3
Create Date: 2025-11-12 18:48:21.107688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '594a754f2d86'
down_revision: Union[str, Sequence[str], None] = 'b0a58a5187a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('atribuido_em', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.alter_column('id',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Integer(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.alter_column('curso_id',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Integer(),
                   existing_nullable=False)
        batch_op.drop_column('data_conclusao')
        batch_op.drop_column('certificado_id')
        batch_op.drop_column('data_validacao')
        batch_op.drop_column('data_atribuicao')

    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lotacao_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('criado_em', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('atualizado_em', sa.DateTime(), nullable=True))
        batch_op.alter_column('id',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Integer(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.alter_column('ano_gd',
                   existing_type=sa.VARCHAR(length=8),
                   type_=sa.Enum('ANO_ATUAL', 'ANO_ANTERIOR', name='anogd'),
                   existing_nullable=True)
        batch_op.drop_column('lotacao')
        batch_op.drop_column('chefia_id')

    with op.batch_alter_table('inscricoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inscrito_em', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.alter_column('id',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Integer(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.alter_column('curso_id',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Integer(),
                   existing_nullable=False)
        batch_op.alter_column('usuario_id', new_column_name='user_id', existing_type=sa.String())
        batch_op.drop_column('data_inscricao')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('inscricoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_inscricao', sa.DATETIME(), nullable=True))
        batch_op.alter_column('user_id', new_column_name='usuario_id', existing_type=sa.String())
        batch_op.alter_column('curso_id',
                   existing_type=sa.Integer(),
                   type_=sa.VARCHAR(),
                   existing_nullable=False)
        batch_op.alter_column('id',
                   existing_type=sa.Integer(),
                   type_=sa.VARCHAR(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.drop_column('inscrito_em')

    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chefia_id', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('lotacao', sa.VARCHAR(), nullable=True))
        batch_op.alter_column('ano_gd',
                   existing_type=sa.Enum('ANO_ATUAL', 'ANO_ANTERIOR', name='anogd'),
                   type_=sa.VARCHAR(length=8),
                   existing_nullable=True)
        batch_op.alter_column('id',
                   existing_type=sa.Integer(),
                   type_=sa.VARCHAR(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.drop_column('atualizado_em')
        batch_op.drop_column('criado_em')
        batch_op.drop_column('lotacao_id')

    with op.batch_alter_table('atribuicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_atribuicao', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('data_validacao', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('certificado_id', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('data_conclusao', sa.DATETIME(), nullable=True))
        batch_op.alter_column('curso_id',
                   existing_type=sa.Integer(),
                   type_=sa.VARCHAR(),
                   existing_nullable=False)
        batch_op.alter_column('id',
                   existing_type=sa.Integer(),
                   type_=sa.VARCHAR(),
                   existing_nullable=False,
                   autoincrement=True)
        batch_op.drop_column('atribuido_em')
