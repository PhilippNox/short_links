from enum import Enum, auto
from pydantic import BaseModel
from typing import Optional


class ReportAdd(BaseModel):
	ok: bool
	msg: Optional[str] = None
	original_url: str
	redirect_url: Optional[str] = None


class ReportLink(BaseModel):
	ok: bool
	link: Optional[str] = None


class InsetDB(Enum):
	OK = auto()
	UNC = auto()
	ERR = auto()


class LinkerGetSrc(Enum):
	RDS = auto()
	DB_OK = auto()
	DB_ERR = auto()


class LinkerReject(Enum):
	RDS = auto()
	DB = auto()
	PASS = auto()
