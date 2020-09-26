from app.config import settings
import sqlalchemy
import databases


DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}" \
			   f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
metadata.create_all(engine)