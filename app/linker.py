
from fastapi.logger import logger

from app.rds.rdsopr import RdsOpr
from app.config import settings
import app.db.crud_redirect as crud_rdir
import app.schemas as schm

import time
from typing import Optional, Tuple, Dict, Any


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

	bag_nolink = TempBag('bag_nolink', 100)
	bag_reject = TempBag('bag_reject', 100)
	ttl = 100

	@classmethod
	async def get_link_or_none(cls, code: str) -> Tuple[Optional[str], schm.LinkerGetSrc]:
		if await cls.bag_nolink.has(code):
			return None, schm.LinkerGetSrc.RDS
		rds_val = await RdsOpr.raw().get(code)
		if rds_val is not None:
			return rds_val, schm.LinkerGetSrc.RDS
		try:
			db_val = await crud_rdir.get_redirect_by_code(code)
			await RdsOpr.raw().setex(code, cls.ttl, db_val)
			return db_val, schm.LinkerGetSrc.DB_OK
		except TypeError as e:
			await cls.bag_nolink.add(code)
			return None, schm.LinkerGetSrc.DB_OK
		except Exception as e:
			logger.warning(f"get_link_or_none - {code} - Exception [{type(e)}]: {e}")
			await cls.bag_nolink.add(code)
			return None, schm.LinkerGetSrc.DB_ERR

