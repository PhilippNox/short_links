from fastapi import Request

from app.config import settings

from pydantic import BaseModel, AnyUrl, ValidationError
from typing import Tuple
import re


class CheckUrl(BaseModel):
	url: AnyUrl


class UrlLogic:

	default_schema = settings.DEFAULT_SCHEMA
	endpoint_set = settings.ENDPOINT_SET
	allowed_schemas = ['http://', 'https://', 'tg://', 'trello://']
	re_schema = r'^[a-zA-Z]+:\/\/'

	@classmethod
	def parser_url(cls, request: Request) -> Tuple[str, str]:
		url = str(request.url)
		url = url[url.find(cls.endpoint_set) + len(cls.endpoint_set):]
		re_out = re.match(cls.re_schema, url)
		if re_out is not None:
			schema = re_out.group(0)
		else:
			schema = settings.DEFAULT_SCHEMA
			url = ''.join([settings.DEFAULT_SCHEMA, url])
		return url, schema

	@classmethod
	def check(cls, url: str, schema: str) -> Tuple[bool, str]:
		if schema not in cls.allowed_schemas:
			return False, f'Schema "{schema}" - is not allowed'
		try:
			CheckUrl(url=url)
			return True, 'ok'
		except ValidationError as e:
			return False, str(e)
