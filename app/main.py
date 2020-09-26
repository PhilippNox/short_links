from fastapi import FastAPI, Cookie, Response
from fastapi.logger import logger

import app.schemas as schm
from app.config import settings
from app.url_checker import UrlChecker

from typing import Optional
import logging
import uuid

app = FastAPI()


# http://127.0.0.1:8000/?url=www.google.com
# http://127.0.0.1:8000/?url=https://www.google.com/
# http://127.0.0.1:8000/?url=https://xn-----glccfbc4ebdaxw3bzag.xn--p1ai/
# http://localhost:8000/?url=https://s.c12.d:123:123:123
# http://localhost:8000/?url=tg://ok.com

@app.get("/")
async def short_link(url: str, response: Response, cookie: Optional[str] = Cookie(None)):
	try:
		# step 0 - cookie
		if cookie is None:
			cookie = str(uuid.uuid4())
			response.set_cookie(key="cookie", value=cookie)

		# step 1 - check url
		url_is_good, url, check_msg = UrlChecker.check(url)
		if url_is_good is False:
			return schm.Report(ok=False, msg=check_msg, original_url=url, cookie=cookie)

		return schm.Report(ok=True, msg='ok', original_url=url, cookie=cookie)

	except Exception as e:
		err_msg = "Sorry, We have a problem here"
		logger.error(f"{err_msg} - {cookie}")
		logger.error(e)
		return schm.Report(
			ok=False,
			msg=err_msg,
			original_url=url,
			cookie=cookie
		)


@app.on_event("startup")
async def startup_event():
	if settings.DEBUG:
		logger.setLevel(logging.DEBUG)


@app.on_event("shutdown")
async def shutdown_event():
	pass
