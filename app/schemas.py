from enum import Enum, auto
from pydantic import BaseModel


class Report(BaseModel):
	ok: bool
	msg: str = ''
	original_url: str
	cookie: str


class InsetDB(Enum):
	OK = auto()
	UNC = auto()
	ERR = auto()
