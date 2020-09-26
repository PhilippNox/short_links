from enum import Enum, auto
from pydantic import BaseModel
from typing import Optional


class ReportAdd(BaseModel):
	ok: bool
	msg: str = ''
	original_url: str
	cookie: str


class ReportLink(BaseModel):
	ok: bool
	link: Optional[str] = None


class InsetDB(Enum):
	OK = auto()
	UNC = auto()
	ERR = auto()
