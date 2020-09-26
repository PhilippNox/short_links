from app.db.core_db import metadata

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

redirect = sa.Table(
	'redirects',
	metadata,
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('created_at', sa.DateTime),
	sa.Column('cookie', UUID),
	sa.Column('code', sa.String(32), nullable=False, unique=True, index=True),
	sa.Column('link', sa.String(2083), nullable=False),
	sa.Column('how_created', JSONB)
)