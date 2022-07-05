"""add foreign key

Revision ID: 2bb9a8c653db
Revises: 6d2699b493fd
Create Date: 2022-07-04 11:21:13.808720

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '2bb9a8c653db'
down_revision = '6d2699b493fd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
