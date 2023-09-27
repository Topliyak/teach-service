from .. import models
from typing import List, NamedTuple


class Contents_Section(NamedTuple):
	name: str
	parent: int | None


class Contents_Page(NamedTuple):
	name: str
	parent: int


class Contents(NamedTuple):
	sections: List[Contents_Section]
	pages: List[Contents_Page]


class SectionWithPK(NamedTuple):
	name: str
	parent__pk: int | None
	pk: int


def get_contents(course_id: int) -> Contents:
	sections_with_pk = _get_sections_with_pk(course_id)

	pages = _get_pages(sections_with_pk)
	sections = _get_sections(sections_with_pk)

	contents = Contents(sections, pages)

	return contents


def _get_sections_with_pk(course_id: int) -> List[SectionWithPK]:
	sections = models.Section.objects.filter(course__id=course_id)\
								.order_by('order')\
								.values('pk', 'name', 'parent__pk')

	return [SectionWithPK(**s) for s in sections]


def _get_sections(sections_with_pk: List[SectionWithPK]) -> List[Contents_Section]:
	sections_pks = []

	sections = []

	for i in range(len(sections_with_pk)):
		section_with_pk = sections_with_pk[i]

		parent_index = None

		if section_with_pk.parent__pk is not None:
			parent_index = sections_pks.index(section_with_pk.parent__pk)

		section = Contents_Section(
			name=section_with_pk.name,
			parent=parent_index,
		)

		sections.append(section)

		sections_pks.append(section_with_pk.pk)

	return sections


def _get_pages(sections: List[SectionWithPK]) -> List[Contents_Page]:
	sections_pk = [s.pk for s in sections]

	ps_with_parent_pk = models.Page.objects.filter(section__pk__in=sections_pk)\
											.exclude(name='')\
											.order_by('order')\
											.values('name', 'section')

	pages = []

	for i, section in enumerate(sections):
		for p in ps_with_parent_pk:
			if p['section'] != section.pk:
				continue

			page = Contents_Page(p['name'], i)
			pages.append(page)

	return pages
