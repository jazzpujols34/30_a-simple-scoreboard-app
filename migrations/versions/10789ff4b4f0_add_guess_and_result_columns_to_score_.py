"""Add guess and result columns to Score table

Revision ID: 10789ff4b4f0
Revises: 6c68fa744625
Create Date: 2023-06-05 11:40:50.473818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10789ff4b4f0'
down_revision = '6c68fa744625'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('guess', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('result', sa.String(length=50), nullable=True))
        batch_op.alter_column('category',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.alter_column('category',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('result')
        batch_op.drop_column('guess')

    # ### end Alembic commands ###