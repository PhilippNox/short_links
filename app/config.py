from pydantic import BaseSettings


class Settings(BaseSettings):
	DEBUG:			bool
	DEFAULT_SCHEMA: str

	class Config:
		env_file = '.env'


settings = Settings()

