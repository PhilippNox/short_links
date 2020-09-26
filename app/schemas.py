from pydantic import BaseModel


class Report(BaseModel):
	ok: bool
	msg: str = ''
	original_url: str
