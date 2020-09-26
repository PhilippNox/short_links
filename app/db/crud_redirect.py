from fastapi.logger import logger

import app.db.models as md
import app.schemas as schm
from app.db.core_db import database

from typing import Optional, Dict, Any
import asyncpg


async def create_redirect(
		code: str,
		link: str,
		cookie: Optional[str] = None,
		how_created: Optional[Dict[str, Any]] = None
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
