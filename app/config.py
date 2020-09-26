from pydantic import BaseSettings


class Settings(BaseSettings):
	DEBUG:			bool
	DEFAULT_SCHEMA: str
	CODE_BASE:		str
	CODE_LEN:		int

	class Config:
		env_file = '.env'


settings = Settings()

