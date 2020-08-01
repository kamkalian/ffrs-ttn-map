"""Change type of lat and lon

Revision ID: 96390c8e1db7
Revises: 152f51ca12e6
Create Date: 2020-08-01 13:25:42.388301

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '96390c8e1db7'
down_revision = '152f51ca12e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('gateway', 'latitude',
               existing_type=mysql.FLOAT(),
               type_=sa.String(length=64),
               existing_nullable=True)
    op.alter_column('gateway', 'longitude',
               existing_type=mysql.FLOAT(),
               type_=sa.String(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('gateway', 'longitude',
               existing_type=sa.String(length=64),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    op.alter_column('gateway', 'latitude',
               existing_type=sa.String(length=64),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    # ### end Alembic commands ###