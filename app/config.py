from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
	DEBUG:			bool
	DEFAULT_SCHEMA: str
	CODE_BASE:		str
	CODE_LEN:		int
	DB_HOST:		str
	DB_PORT:		str
	DB_USER:		str
	DB_PASSWORD:	str
	DB_DATABASE:	str
	REDIS_DNS:		RedisDsn

	class Config:
		env_file = '.env'


settings = Settings()

