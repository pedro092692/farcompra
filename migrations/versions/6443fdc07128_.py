"""empty message

Revision ID: 6443fdc07128
Revises: c81a0065b585
Create Date: 2024-07-09 15:44:05.329650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6443fdc07128'
down_revision = 'c81a0065b585'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.drop_column('laboratory_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('laboratory_name', sa.VARCHAR(length=250), nullable=False))

    # ### end Alembic commands ###
