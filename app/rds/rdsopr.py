from fastapi.logger import logger

from app.config import settings

import aioredis


class RdsOpr:

	rds = None

	@classmethod
	async def start(cls):
		cls.rds = await aioredis.create_redis_pool(
			settings.REDIS_DNS,
			encoding='utf-8'
		)
		logger.info(f"RdsOpr 💾 : redis - start")

	@classmethod
	async def stop(cls):
		cls.rds.close()
		return await cls.rds.wait_closed()

	@classmethod
	def raw(cls):
		return cls.rds
