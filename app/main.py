from fastapi import FastAPI, Cookie, Response
from fastapi.logger import logger
from fastapi.responses import RedirectResponse

import app.schemas as schm
from app.config import settings
from app.url_checker import UrlChecker
from app.rnd_code import RndCode
from app.db.core_db import database
from app.rds.rdsopr import RdsOpr
from app.linker import Linker

from typing import Optional
import logging
import uuid

app = FastAPI()
host = settings.HOST

# http://127.0.0.1:8000/?url=www.ya.ru
# http://127.0.0.1:8000/?url=tg://resolve?domain=techsparks
# http://127.0.0.1:8000/?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ


@app.get("/")
async def short_link(url: str, response: Response, cookie: Optional[str] = Cookie(None)):
	try:
		# step 0 - cookie
		if cookie is None:
			cookie = str(uuid.uuid4())
			response.set_cookie(key="cookie", value=cookie, max_age=315576000)

		# step 1 - check url
		url_is_good, url, check_msg = UrlChecker.check(url)
		if url_is_good is False:
			return schm.ReportAdd(ok=False, msg=check_msg, original_url=url)

		# step 2 - generate a code
		reject = dict()
		for _ in range(settings.REJECT_LIM):
			rnd = RndCode.get_rnd()
			rjc = await Linker.add_redirect(code=rnd, link=url, cookie=cookie, how_created=reject)
			if rjc is schm.LinkerReject.PASS:
				return schm.ReportAdd(
					ok=True, msg='ok', original_url=url, redirect_url=f'{host}{rnd}')
			reject[rjc] = reject.get(rjc, 0) + 1
		logger.warning(f"REJECT_LIM - {cookie} - {url}")
		return schm.ReportAdd(ok=False, msg=settings.MSG_REJECT, original_url=url)

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
