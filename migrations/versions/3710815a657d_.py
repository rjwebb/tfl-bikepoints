"""empty message

Revision ID: 3710815a657d
Revises: 1d7d6fe675a9
Create Date: 2015-12-12 20:48:42.213324

"""

# revision identifiers, used by Alembic.
revision = '3710815a657d'
down_revision = '1d7d6fe675a9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bikepoints', sa.Column('name', sa.String(), nullable=True))
    op.drop_column('bikepoints', 'id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bikepoints', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_column('bikepoints', 'name')
    ### end Alembic commands ###
