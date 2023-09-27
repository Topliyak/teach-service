from django.contrib.auth.models import User
from ...models import Course, Section, Page
from typing import Dict, List

from ._sections import (
	edit_sections,
	add_sections,
	delete_sections_and_get_deleted,
	SectionStruct,
	validate_sections,
)

from ._pages import (
	edit_pages,
	add_pages,
	delete_pages,
	validate_pages,
	PageStruct,
	IndexesAndPages,
)


def edit_course(course_id: int, editor: User, **edits):
	course = Course.objects.get(pk=course_id)

	sections: List[Section]
	sections_queryset = course.section_set.select_related('parent').all()
	sections = list(sections_queryset)

	indexes_and_sections: Dict[int, SectionStruct]
	indexes_and_sections = _get_indexes_sections(sections)

	if _has_edit_permission(course, editor) is False:
		raise ValueError() # user hasnt edit permission

	if 'name' in edits:
		course.name = edits['name']

	deleted = []

	if 'delete_sections' in edits:
		deleted = delete_sections_and_get_deleted(indexes_and_sections, edits['delete_sections'])

	if 'edit_sections' in edits:
		edit_sections(indexes_and_sections, edits['edit_sections'])

	if 'new_sections' in edits:
		add_sections(course, edits['new_sections'], indexes_and_sections)

	pages: List[Page]
	pages_queryset = Page.objects.filter(section__in=sections_queryset).select_related('section')
	pages = list(pages_queryset)

	indexes_and_pages = _get_indexes_and_pages(pages, indexes_and_sections)

	deleted_pages = []

	if 'delete_pages' in edits:
		deleted_pages = delete_pages(indexes_and_pages, edits['delete_pages'])

	if 'edit_pages' in edits:
		edit_pages(indexes_and_pages, edits['edit_pages'])

	if 'new_pages' in edits:
		add_pages(indexes_and_pages, edits['new_pages'])

	validate_pages(indexes_and_pages, raise_exception=True)
	validate_sections(indexes_and_sections, indexes_and_pages.values(), raise_exception=True)

	confirm_changes(course, indexes_and_sections, sections, deleted)


def _has_edit_permission(course: Course, editor: User) -> bool:
	if course.author == editor:
		return True

	return False


def _get_indexes_sections(sections: List[Section]) -> Dict[int, SectionStruct]:
	indexes_and_sections = {}

	for section in sections:
		index = section.order
		parent = None

		if section.parent is not None:
			parent = section.parent.order

		sstruct = SectionStruct(
			pk=section.pk,
			name=section.name,
			parent_index=parent,
		)

		indexes_and_sections[index] = sstruct

	return indexes_and_sections


def _get_indexes_and_pages(
		pages: List[Page],
		indexes_and_sections: Dict[int, SectionStruct]) -> IndexesAndPages:
	indexes_and_pages = {}
	section_pks_and_indexes = {s.pk: i for i, s in indexes_and_sections.items()}

	for page in pages:
		section_index = section_pks_and_indexes[page.section.pk]
		pstruct = PageStruct(
			pk=page.pk,
			name=page.name,
			section_index=section_index,
			content=page.content,
			answer=None,
		)

		indexes_and_pages[page.order] = pstruct

	return indexes_and_pages


def confirm_changes(
		course: Course,
		indexes_and_sections: Dict[int, SectionStruct],
		sections: List[Section],
		deleted: List[SectionStruct]) -> None:

	course.save()

	indexes_and_pks: Dict[int, int]
	indexes_and_pks = {}

	for i, sstruct in indexes_and_sections.items():
		if sstruct.pk is not None:
			indexes_and_pks[i] = sstruct.pk
			continue

		instnc = Section.objects.create(
			course=course,
			order=i,
			name=sstruct.name,
			parent=None,
		)

		sstruct.pk = instnc.pk
		sections.append(instnc)

		indexes_and_pks[i] = instnc.pk

	pks_and_sections: Dict[int, Section]
	pks_and_sections = {s.pk: s for s in sections}

	for i, sstruct in indexes_and_sections.items():
		parent = None

		if sstruct.parent_index is not None:
			parent_index = sstruct.parent_index
			parent_pk = indexes_and_pks[parent_index]
			parent = pks_and_sections[parent_pk]

		section = pks_and_sections[sstruct.pk]

		section.name = sstruct.name
		section.parent = parent
		section.order = i

		section.save()

	for d in deleted:
		pks_and_sections[d.pk].delete()
