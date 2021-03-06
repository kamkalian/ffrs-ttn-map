"""Added owner to gateway

Revision ID: ace2d84e5e1b
Revises: a6e6fe76b76f
Create Date: 2020-03-25 19:54:32.471859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ace2d84e5e1b'
down_revision = 'a6e6fe76b76f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gateway', sa.Column('owner', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_gateway_owner'), 'gateway', ['owner'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gateway_owner'), table_name='gateway')
    op.drop_column('gateway', 'owner')
    # ### end Alembic commands ###
