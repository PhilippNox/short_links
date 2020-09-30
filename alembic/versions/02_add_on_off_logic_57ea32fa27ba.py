"""02_add_on_off_logic

Revision ID: 57ea32fa27ba
Revises: f766bae1853c
Create Date: 2020-09-30 16:39:40.648697

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '57ea32fa27ba'
down_revision = 'f766bae1853c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('redirects', sa.Column('is_on', sa.Boolean(), server_default='True'))
    op.add_column('redirects', sa.Column('who_switched', UUID))


def downgrade():
    op.drop_column('redirects', 'is_on')
    op.drop_column('redirects', 'who_switched')

