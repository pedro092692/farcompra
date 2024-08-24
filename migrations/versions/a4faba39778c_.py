"""empty message

Revision ID: a4faba39778c
Revises: 803028952ef2
Create Date: 2024-08-24 12:05:39.928219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4faba39778c'
down_revision = '803028952ef2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode', sa.String(length=250), nullable=True))
        batch_op.create_unique_constraint('barcode', ['barcode'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('barcode')

    # ### end Alembic commands ###
