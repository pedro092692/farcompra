"""empty message

Revision ID: 6cec1638154d
Revises: 11669922604f
Create Date: 2024-07-09 15:51:04.762087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cec1638154d'
down_revision = '11669922604f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_price_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('supplier_name', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('product_name', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('product_price', sa.Float(), nullable=False))
        batch_op.drop_column('supplier_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoppingcart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('supplier_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'suppliers', ['supplier_id'], ['id'])
        batch_op.drop_column('product_price')
        batch_op.drop_column('product_name')
        batch_op.drop_column('supplier_name')
        batch_op.drop_column('product_price_id')

    # ### end Alembic commands ###