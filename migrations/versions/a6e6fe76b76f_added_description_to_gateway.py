"""Added description to gateway

Revision ID: a6e6fe76b76f
Revises: 81c4f42a30c6
Create Date: 2020-03-25 19:49:56.529388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6e6fe76b76f'
down_revision = '81c4f42a30c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gateway', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gateway', 'description')
    # ### end Alembic commands ###