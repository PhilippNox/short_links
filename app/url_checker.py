from app.config import settings

from pydantic import BaseModel, AnyUrl, ValidationError

from typing import Tuple
import re


class CheckUrl(BaseModel):
	url: AnyUrl


class UrlChecker:

	default_schema = settings.DEFAULT_SCHEMA
	re_schema = r'^[a-zA-Z]+:\/\/'
	allowed_schemas = ['http://', 'https://', 'tg://', 'trello://']

	@classmethod
	def check(cls, url: str) -> Tuple[bool, str, str]:
		re_out = re.match(cls.re_schema, url)
		if re_out is not None:
			schema = re_out.group(0)
		else:
			schema = cls.default_schema
			url = ''.join([cls.default_schema, url])
		if schema not in cls.allowed_schemas:
			return False, url, f'Schema "{schema}" - is not allowed'

		try:
			CheckUrl(url=url)
			return True, url, 'ok'
		except ValidationError as e:
			return False, url, str(e)
