"""01_create_redirects

Revision ID: f766bae1853c
Revises: 
Create Date: 2020-09-26 20:05:06.537762

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# For utcnow
# https://docs.sqlalchemy.org/en/13/core/compiler.html#utc-timestamp-function
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# revision identifiers, used by Alembic.
revision = 'f766bae1853c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'redirects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=utcnow()),
        sa.Column('cookie', UUID),
        sa.Column('code', sa.String(32), nullable=False, unique=True, index=True),
        sa.Column('link', sa.String(2083), nullable=False),
        sa.Column('how_created', JSONB)
    )


def downgrade():
    op.drop_table('redirects')
