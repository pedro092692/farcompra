"""empty message

Revision ID: c81a0065b585
Revises: 
Create Date: 2024-07-09 15:37:21.455155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81a0065b585'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('laboratory_name', sa.String(length=250), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.drop_column('laboratory_name')

    # ### end Alembic commands ###
