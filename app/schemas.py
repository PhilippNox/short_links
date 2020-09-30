from enum import Enum, auto
from pydantic import BaseModel
from typing import Optional


class ReportAdd(BaseModel):
	ok: 			bool
	msg: 			Optional[str] = None
	request_url: 	str
	target_url: 	Optional[str] = None
	redirect_url: 	Optional[str] = None


class ReportLink(BaseModel):
	ok: 			bool
	link: 			Optional[str] = None
	is_on:			Optional[str] = None


class ReportSimple(BaseModel):
	ok:				bool


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
