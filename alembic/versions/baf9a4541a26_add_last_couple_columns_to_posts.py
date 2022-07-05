"""add_last_couple_columns_to_posts

Revision ID: baf9a4541a26
Revises: 2bb9a8c653db
Create Date: 2022-07-04 11:28:50.222541

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = 'baf9a4541a26'
down_revision = '2bb9a8c653db'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='True'))


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
