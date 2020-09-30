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
endpoint_set = '/set'
endpoint_with = '/set_with'

# http://127.0.0.1:8000/set/www.ya.ru
# http://127.0.0.1:8000/set/tg://resolve?domain=techsparks
# http://127.0.0.1:8000/set/https://www.youtube.com/watch?v=dQw4w9WgXcQ


def process_cookie(response: Response, cookie: Optional[str] = Cookie(None)):
	if cookie is None:
		cookie = str(uuid.uuid4())
		response.set_cookie(key="cookie", value=cookie, max_age=315576000)


@app.get(endpoint_set + "/{foo:path}")
async def set_link(rqt: Request, rsp: Response, cookie: Optional[str] = Cookie(None)):
	try:
		# step 0 - get url
		url, schema = UrlLogic.parser_url(full_url=str(rqt.url), endpoint=endpoint_set)

		# step 1 - check and add cookie
		process_cookie(rsp, cookie)

		# step 2 - check url
		url_is_good, check_msg = UrlLogic.check(url, schema)
		if url_is_good is False:
			return schm.ReportAdd(ok=False, msg=check_msg, request_url=str(rqt.url))

		# step 3 - generate a code
		added, code = await Linker.gen_code_add_link(url, cookie)
		if added is False:
			return schm.ReportAdd(ok=False, msg=settings.MSG_REJECT, request_url=str(rqt.url))
		return schm.ReportAdd(
			ok=True,
			msg='ok',
			request_url=str(rqt.url),
			target_url=url,
			redirect_url=f'{host}{code}'
		)

	except Exception as e:
		err_msg = settings.MSG_FAIL
		logger.error(f"{err_msg} - {cookie}")
		logger.error(e)
		return schm.ReportAdd(ok=False, msg=err_msg, request_url=str(rqt.url))


@app.get(endpoint_with + "/{given}/{foo:path}")
async def set_with(given: str, rqt: Request, rsp: Response, cookie: Optional[str] = Cookie(None)):
	try:
		# step 0 - get url
		url, schema = UrlLogic.parser_url(full_url=str(rqt.url), endpoint=endpoint_with, name=given)

		# step 1 - check and add cookie
		process_cookie(rsp, cookie)

		# step 2 - check url
		url_is_good, check_msg = UrlLogic.check(url, schema)
		if url_is_good is False:
			return schm.ReportAdd(ok=False, msg=check_msg, request_url=str(rqt.url))

		# step 3 - try to add
		rlt = await Linker.add_redirect(code=given, link=url, cookie=cookie)
		if rlt is not schm.LinkerReject.PASS:
			return schm.ReportAdd(ok=False, msg=settings.MSG_REJECT, request_url=str(rqt.url))
		return schm.ReportAdd(
			ok=True,
			msg='ok',
			request_url=str(rqt.url),
			target_url=url,
			redirect_url=f'{host}{given}'
		)

	except Exception as e:
		err_msg = settings.MSG_FAIL
		logger.error(f"{err_msg} - {cookie}")
		logger.error(e)
		return schm.ReportAdd(ok=False, msg=err_msg, request_url=str(rqt.url))


# http://localhost:8000/get/Xn87

@app.get("/get/{code}")
async def get_info_link(code: str):
	try:
		redirect, src = await Linker.get_link_or_none(code)
		logger.debug(f'Linker return - {code} - {redirect} - {src}')
		if redirect is None:
			return schm.ReportLink(ok=False)
		return schm.ReportLink(ok=True, link=redirect['link'], is_on=redirect['is_on'])
	except Exception as e:
		logger.warning(f"get_link - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportLink(ok=False)


# http://localhost:8000/Xn87

@app.get("/{code}")
async def get_link(code: str):
	try:
		redirect, src = await Linker.get_link_or_none(code)
		logger.debug(f'Linker return - {code} - {redirect} - {src}')
		if redirect is None:
			return schm.ReportLink(ok=False)
		if redirect['is_on'] is '0':
			return schm.ReportLink(ok=True, link=redirect['link'], is_on=redirect['is_on'])
		return RedirectResponse(redirect['link'])
	except Exception as e:
		logger.warning(f"get_link - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportLink(ok=False)


@app.get("/")  # todo add main page html
async def simple():
	return {'ok': True, 'msg': 'check readme file'}


@app.get("/turn_on/{code}")
async def turn_on(code: str):
	try:
		out = await Linker.switch_on_state(code=code, turn_on=True)
		return schm.ReportSimple(ok=True) if out else schm.ReportSimple(ok=False)
	except Exception as e:
		logger.warning(f"turn_on - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportSimple(ok=False)


@app.get("/turn_off/{code}")
async def turn_on(code: str):
	try:
		out = await Linker.switch_on_state(code=code, turn_on=False)
		return schm.ReportSimple(ok=True) if out else schm.ReportSimple(ok=False)
	except Exception as e:
		logger.warning(f"turn_on - {code} - Exception [{type(e)}]: {e}")
		return schm.ReportSimple(ok=False)


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
