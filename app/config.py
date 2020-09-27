from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
	DEBUG:			bool
	DEFAULT_SCHEMA: str
	CODE_BASE:		str
	CODE_LEN:		int
	HOST:			str
	DB_HOST:		str
	DB_PORT:		str
	DB_USER:		str
	DB_PASSWORD:	str
	DB_DATABASE:	str
	REDIS_DNS:		RedisDsn
	RDS_TTL_REJECT:	int = 100
	RDS_TTL_NOLINK:	int = 3600
	RDS_TTL_CACHE:	int = 3600
	REJECT_LIM:		int
	MSG_REJECT:		str = "Reject by a limit of try to generate code"
	MSG_FAIL:		str = "Sorry, We have a problem here"

	class Config:
		env_file = '.env'


settings = Settings()

