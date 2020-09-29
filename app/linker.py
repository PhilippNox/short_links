
from fastapi.logger import logger

from app.config import settings
from app.rds.rdsopr import RdsOpr
from app.rnd_code import RndCode
import app.db.crud_redirect as crud_rdir
import app.schemas as schm

from typing import Optional, Tuple, Dict, Any
import time


class TempBag:

	def __init__(self, rdn_name: str, ttl: int):
		self.rds_name = rdn_name
		self.ttl = ttl

	async def add(self, elem: str):
		utc = time.time()
		logger.debug(f'TempBag - {self.rds_name} - {self.ttl} - {utc} - {elem}')
		await RdsOpr.raw().zadd(self.rds_name, utc, elem)
		await RdsOpr.raw().zremrangebyscore(self.rds_name, max=utc-self.ttl)
		await RdsOpr.raw().expire(self.rds_name, self.ttl)

	async def has(self, elem: str) -> bool:
		return await RdsOpr.raw().zrank(self.rds_name, elem) is not None

	async def rem(self, elem: str):
		await RdsOpr.raw().zrem(self.rds_name, elem)


class Linker:

	bag_nolink = TempBag('bag_nolink', settings.RDS_TTL_NOLINK)
	bag_reject = TempBag('bag_reject', settings.RDS_TTL_REJECT)
	cache_ttl = settings.RDS_TTL_CACHE

	@classmethod
	async def get_link_or_none(cls, code: str) -> Tuple[Optional[str], schm.LinkerGetSrc]:
		if await cls.bag_nolink.has(code):
			return None, schm.LinkerGetSrc.RDS
		rds_val = await RdsOpr.raw().get(code)
		if rds_val is not None:
			return rds_val, schm.LinkerGetSrc.RDS
		try:
			db_val = await crud_rdir.get_redirect_by_code(code)
			await RdsOpr.raw().setex(code, cls.cache_ttl, db_val)
			return db_val, schm.LinkerGetSrc.DB_OK
		except TypeError as e:
			await cls.bag_nolink.add(code)
			return None, schm.LinkerGetSrc.DB_OK
		except Exception as e:
			logger.warning(f"get_link_or_none - {code} - Exception [{type(e)}]: {e}")
			await cls.bag_nolink.add(code)
			return None, schm.LinkerGetSrc.DB_ERR

	@classmethod
	async def add_redirect(
			cls,
			code: str,
			link: str,
			cookie: Optional[str] = None,
			how_created: Optional[Dict[schm.LinkerReject, Any]] = None
	) -> schm.LinkerReject:
		if await cls.bag_reject.has(code):
			return schm.LinkerReject.RDS
		db = await crud_rdir.create_redirect(
			code=code,
			link=link,
			cookie=cookie,
			how_created=how_created)
		if db is schm.InsetDB.OK:
			await cls.bag_nolink.rem(code)
			await cls.bag_reject.rem(code)
			await RdsOpr.raw().setex(code, cls.cache_ttl, link)
			return schm.LinkerReject.PASS
		else:
			await cls.bag_reject.add(code)
			return schm.LinkerReject.DB

	@classmethod
	async def gen_code_add_link(cls, url: str, cookie: str) -> Tuple[bool, Optional[str]]:
		reject = dict()  # reject history
		for _ in range(settings.REJECT_LIM):
			rnd = RndCode.get_rnd()
			rjc = await Linker.add_redirect(code=rnd, link=url, cookie=cookie, how_created=reject)
			if rjc is schm.LinkerReject.PASS:
				return True, rnd
			reject[rjc] = reject.get(rjc, 0) + 1
		logger.warning(f"REJECT_LIM - {cookie} - {url}")
		return False, None
