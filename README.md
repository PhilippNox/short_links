
cp .env_example .env
setup .env

uvicorn app.main:app --reload --port 8000
