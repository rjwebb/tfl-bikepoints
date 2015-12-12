"""empty message

Revision ID: b70f9184648
Revises: None
Create Date: 2015-12-12 20:00:01.839248

"""

# revision identifiers, used by Alembic.
revision = 'b70f9184648'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bikepoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bp_id', sa.String(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('nbDocks', sa.Integer(), nullable=True),
    sa.Column('nbBikes', sa.Integer(), nullable=True),
    sa.Column('nbEmptyDocks', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'bp_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bikepoints')
    ### end Alembic commands ###