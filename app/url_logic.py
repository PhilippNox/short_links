from fastapi import Request

from app.config import settings

from pydantic import BaseModel, AnyUrl, ValidationError
from typing import Tuple
import re


class CheckUrl(BaseModel):
	url: AnyUrl


class UrlLogic:

	default_schema = settings.DEFAULT_SCHEMA
	allowed_schemas = settings.ALLOWED_SCHEMAS
	re_schema = r'^[a-zA-Z]+:\/\/'

	@classmethod
	def parser_url(cls, full_url: str, endpoint: str, name: str = '') -> Tuple[str, str]:
		shift = len(name) + 2 if name != '' else 1  # in case '' 1 slash else 2 slashes
		trg = full_url[full_url.find(endpoint) + len(endpoint) + shift:]
		re_out = re.match(cls.re_schema, trg)
		if re_out is not None:
			schema = re_out.group(0)
		else:
			schema = settings.DEFAULT_SCHEMA
			trg = ''.join([settings.DEFAULT_SCHEMA, trg])
		return trg, schema

	@classmethod
	def check(cls, url: str, schema: str) -> Tuple[bool, str]:
		if cls.allowed_schemas is not None and schema not in cls.allowed_schemas:
			return False, f'Schema "{schema}" - is not allowed'
		try:
			CheckUrl(url=url)
			return True, 'ok'
		except ValidationError as e:
			return False, str(e)
