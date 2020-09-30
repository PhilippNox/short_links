from fastapi.logger import logger

import app.db.models as md
import app.schemas as schm
from app.db.core_db import database

from typing import Optional, Dict, Any, Tuple
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


# not -> [str, bool] cause rds cant save bool in hash
async def get_redirect_by_code(code: str) -> Tuple[str, str]:
	query = sa.select([md.redirect.c.link, md.redirect.c.is_on]).where(md.redirect.c.code == code)
	out = await database.fetch_one(query=query)
	return out['link'], '1' if out['is_on'] else '0'


async def update_on_state(code: str, turn_on: bool) -> bool:
	try:
		query = md.redirect.update()\
			.where(md.redirect.c.code == code)\
			.values(is_on=turn_on)\
			.returning(md.redirect.c.code)
		out = await database.execute(query)
		return True if out is not None else False
	except Exception as e:
		logger.warning(f"update_on_state - {code} - Exception [{type(e)}]: {e}")
		return False
