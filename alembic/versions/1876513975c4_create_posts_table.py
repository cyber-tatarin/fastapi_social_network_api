"""create posts table

Revision ID: 1876513975c4
Revises: 
Create Date: 2022-07-04 10:44:04.842868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1876513975c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
