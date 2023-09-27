from ... import models
from typing import NamedTuple, List, Dict


class SectionStruct(NamedTuple):
	name: str
	parent: int


class PageStruct(NamedTuple):
	parent: int
	name: str | None
	content: str
	answer: Dict


class CourseStruct(NamedTuple):
	name: str
	sections: List[SectionStruct]
	pages: List[PageStruct]


def try_add_course(name: str, sections_dicts: List[Dict], pages_dicts: List[Dict], author: int):
	sections = _get_sections(sections_dicts)
	pages = _get_pages(pages_dicts)
	course = CourseStruct(name, sections, pages)

	if _is_valid_course(course) is False:
		raise ValueError('Not valid data')

	_post(course, author)


def _post(course: CourseStruct, author: int):
	posted_course = models.Course.objects.create(
		name=course.name,
		author=author,
		access_limiter=None,
	)

	published_sections = _post_sections(course.sections, posted_course)
	_post_pages(course.pages, published_sections)


def _post_sections(sections: List[SectionStruct], course: int) -> List[int]:
	published_sections = []

	for i in range(len(sections)):
		section = sections[i]

		parent_pk = None

		if section.parent is not None:
			parent_pk = published_sections[section.parent]

		posted_section = models.Section.objects.create(
			course=course,
			parent=parent_pk,
			name=section.name,
			order=i,
		)

		published_sections.append(posted_section)

	return published_sections


def _post_pages(pages: List[PageStruct], published_sections: List[int]):
	for i in range(len((pages))):
		page = pages[i]
		parent = published_sections[page.parent]

		models.Page.objects.create(
			order=i,
			content=page.content,
			name=page.name,
			section=parent,
			answer=None,
		)


def _get_sections(sections_dicts: List[Dict]) -> List[SectionStruct]:
	sections = []

	for sd in sections_dicts:
		s = SectionStruct(**sd)
		sections.append(s)

	return sections


def _get_pages(pages_dicts: List[Dict]) -> List[PageStruct]:
	pages = []

	for pd in pages_dicts:
		p = PageStruct(**pd)
		pages.append(p)

	return pages


def _is_valid_course(course: CourseStruct) -> bool:
	validations = [
		_check_sections_tree_is_not_looped(course.sections),
		_check_that_parents_only_for_sections_or_only_for_pages(course.sections, course.pages),
	]

	return all(validations)


def _check_sections_tree_is_not_looped(sections: List[SectionStruct]) -> bool:
	for i in range(len(sections)):
		parent_index = sections[i].parent

		if parent_index is None:
			continue

		if not (0 <= parent_index < i):
			return False

	return True


def _check_that_parents_only_for_sections_or_only_for_pages(
		sections: List[SectionStruct],
		pages: List[PageStruct]) -> bool:

	sections_for_pages = set([page.parent for page in pages])

	for section in sections:
		if section.parent in sections_for_pages:
			return False

	return True
