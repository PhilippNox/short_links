from fastapi.logger import logger

import app.db.models as md
import app.schemas as schm
from app.db.core_db import database

from typing import Optional, Dict, Any
import sqlalchemy as sa
import asyncpg


async def create_redirect(
		code: str,
		link: str,
		cookie: Optional[str] = None,
		how_created: Optional[Dict[schm.LinkerReject, Any]] = None
) -> schm.InsetDB:
	try:
		query = md.redirect.insert().values(
			code=code,
			link=link,
			cookie=cookie,
			how_created=how_created
		)
		await database.execute(query)
		return schm.InsetDB.OK
	except asyncpg.exceptions.UniqueViolationError as e:
		logger.warning(f"crud_redirect - {cookie} - {code} - 🎯💽 - unique_hit")
		return schm.InsetDB.UNC
	except Exception as e:
		logger.warning(f"crud_redirect - {cookie} - {code} - ❌💽 - Exception [{type(e)}]: {e}")
		return schm.InsetDB.ERR


async def get_redirect_by_code(code: str) -> str:
	query = sa.select([md.redirect.c.link]).where(md.redirect.c.code == code)
	out = await database.fetch_one(query=query)
	return out['link']

