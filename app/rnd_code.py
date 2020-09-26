from app.config import settings
import random


class RndCode:

	code_base = settings.CODE_BASE
	code_len = settings.CODE_LEN

	@classmethod
	def get_rnd(cls) -> str:
		out = []
		idx = 0
		while idx < cls.code_len:
			out.append(random.choice(cls.code_base))
			idx += 1
		return ''.join(out)

