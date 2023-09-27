from .. import models
from server.apps.answers.services import get_answer_struct
from typing import NamedTuple, Dict


class Page(NamedTuple):
	name: str
	content: str
	answer: Dict


def get_page(course: int, num: int):
	pages_qs = models.Page.objects.filter(section__course__pk=course)\
								.order_by('order')\
								.values_list('name', 'content', 'answer')

	if not (0 <= num < len(pages_qs)):
		raise ValueError(f'There is not page {num}')

	page = pages_qs[num]

	answer = None

	if page[2] is not None:
		answer = get_answer_struct(page[2])

	return Page(
		name=page[0],
		content=page[1],
		answer=answer
	)
