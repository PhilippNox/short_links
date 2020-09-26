from pydantic import BaseSettings


class Settings(BaseSettings):
	DEBUG:			bool

	class Config:
		env_file = '.env'


settings = Settings()

