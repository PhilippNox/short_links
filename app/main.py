from fastapi import FastAPI
from fastapi.logger import logger

import app.schemas as schm
from app.config import settings

import logging


app = FastAPI()


# http://127.0.0.1:8000/?url=www.google.com
# http://127.0.0.1:8000/?url=https://www.google.com/
# http://127.0.0.1:8000/?url=https://xn-----glccfbc4ebdaxw3bzag.xn--p1ai/
# http://localhost:8000/?url=https://s.c12.d:123:123:123
# http://localhost:8000/?url=tg://ok.com

@app.get("/")
async def short_link(url: str):
	try:
		return schm.Report(ok=True, msg='ok', original_url=url)

	except Exception as e:
		err_msg = "Sorry, We have a problem here"
		logger.error(f"{err_msg}")
		logger.error(e)
		return schm.Report(
			ok=False,
			msg=err_msg,
			original_url=url,
		)


@app.on_event("startup")
async def startup_event():
	if settings.DEBUG:
		logger.setLevel(logging.DEBUG)


@app.on_event("shutdown")
async def shutdown_event():
	pass
