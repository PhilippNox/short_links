from fastapi import FastAPI, Cookie, Response, Request
from fastapi.logger import logger
from fastapi.responses import RedirectResponse

import app.schemas as schm
from app.config import settings
from app.url_logic import UrlLogic
from app.db.core_db import database
from app.rds.rdsopr import RdsOpr
from app.linker import Linker

from typing import Optional
import logging
import uuid

app = FastAPI()
host = settings.HOST


# http://127.0.0.1:8000/set/www.ya.ru
# http://127.0.0.1:8000/set/tg://resolve?domain=techsparks
# http://127.0.0.1:8000/set/https://www.youtube.com/watch?v=dQw4w9WgXcQ

def process_cookie(response: Response, cookie: Optional[str] = Cookie(None)):
	if cookie is None:
		cookie = str(uuid.uuid4())
		response.set_cookie(key="cookie", value=cookie, max_age=315576000)


@app.get(settings.ENDPOINT_SET + "{foo:path}")
async def short_link(request: Request, response: Response, cookie: Optional[str] = Cookie(None)):
	# step 0 - get url
	url, schema = UrlLogic.parser_url(request)
	try:
		# step 1 - check and add cookie
		process_cookie(response, cookie)

		# step 2 - check url
		url_is_good, check_msg = UrlLogic.check(url, schema)
		if url_is_good is False:
			return schm.ReportAdd(ok=False, msg=check_msg, original_url=url)

		# step 3 - generate a code
		added, code = await Linker.gen_code_add_link(url, cookie)
		if added is False:
			return schm.ReportAdd(ok=False, msg=settings.MSG_REJECT, original_url=url)
		return schm.ReportAdd(ok=True, msg='ok', original_url=url, redirect_url=f'{host}{code}')

	except Exception as e:
		err_msg = settings.MSG_FAIL
		logger.error(f"{err_msg} - {cookie}")
		logger.error(e)
		return schm.ReportAdd(ok=False, msg=err_msg, original_url=url)


# http://localhost:8000/get/Xn87

@app.get("/get/{code}")
async def get_link(code: str):
	try:
		link, src = await Linker.get_link_or_none(code)
		logger.debug(f'Linker return - {link} - {src}')
		if link is None:
			return schm.ReportLink(ok=False)
		return schm.ReportLink(ok=True, link=link)
	except Exception as e:
		logger.warning(f"get_link - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportLink(ok=False)


# http://localhost:8000/Xn87

@app.get("/{code}")
async def get_link(code: str):
	try:
		link, src = await Linker.get_link_or_none(code)
		logger.debug(f'Linker return - {link} - {src}')
		if link is None:
			return schm.ReportLink(ok=False)
		return RedirectResponse(link)
	except Exception as e:
		logger.warning(f"get_link - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportLink(ok=False)


@app.on_event("startup")
async def startup_event():
	if settings.DEBUG:
		logger.setLevel(logging.DEBUG)
	await database.connect()
	await RdsOpr.start()


@app.on_event("shutdown")
async def shutdown_event():
	await database.disconnect()
	await RdsOpr.stop()
