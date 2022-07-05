"""add content column to posts table

Revision ID: aa2fc0fd991d
Revises: 1876513975c4
Create Date: 2022-07-04 10:59:22.085580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2fc0fd991d'
down_revision = '1876513975c4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
