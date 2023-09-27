from ...models import Course
from typing import List, NamedTuple, Dict, Optional, Iterable
from dataclasses import dataclass
from ._pages import PageStruct


@dataclass
class SectionStruct:
	pk: int | None
	name: str
	parent_index: Optional[int]


class SectionEdit(NamedTuple):
	index: int
	name: Optional[str] = None
	new_index: Optional[int] = None
	parent_index: Optional[int] = None


class SectionNew(NamedTuple):
	course: Course
	index: int
	name: str
	parent: int


def delete_sections_and_get_deleted(
		indexes_and_sections: Dict[int, SectionStruct],
		indexes: List[int]) -> List[SectionStruct]:

	indexes_set = set(indexes)
	deleted = []

	sections: List[SectionStruct | None]
	sections = [None] * (len(indexes_and_sections) - len(indexes_set))
	pos = 0

	for i in range(len(indexes_and_sections)):
		s = indexes_and_sections[i]

		if i in indexes_set:
			deleted.append(s)
			continue

		sections[pos] = s
		pos += 1

	indexes_and_sections.clear()

	for i, s in enumerate(sections):
		indexes_and_sections[i] = s

	return deleted


def edit_sections(indexes_and_sections: Dict[int, SectionStruct], edits: List[Dict]) -> None:
	new_old_indexes = {}

	for edict in edits:
		edit = SectionEdit(**edict)

		index = edit.index
		section = indexes_and_sections[index]
		_edit_order_independent_fields_of_section(edit, section)

		if edit.new_index is not None:
			new_old_indexes[edit.new_index] = edit.index

	_reorder_sections(indexes_and_sections, new_old_indexes)


def _reorder_sections(
		indexes_and_sections: Dict[int, SectionStruct],
		new_old_indexes: Dict[int, int]) -> None:

	sections: List[SectionStruct | None]
	sections = [None] * len(indexes_and_sections)

	for i in range(len(sections)):
		if i in new_old_indexes:
			old_index = new_old_indexes[i]
			sections[i] = indexes_and_sections[old_index]

	pos = 0
	old_indexes = set(new_old_indexes.values())

	for i in indexes_and_sections:
		if i not in old_indexes:
			sections[pos] = indexes_and_sections[i]

			while pos < len(sections):
				pos += 1

				if sections[pos] is None:
					break

	for i in indexes_and_sections:
		indexes_and_sections[i] = sections[i]


def _edit_order_independent_fields_of_section(edit: SectionEdit, section: SectionStruct):
	if edit.name is not None:
		section.name = edit.name

	if edit.parent_index is not None:
		section.parent_index = edit.parent_index


def add_sections(
		course: Course,
		new_elements: List[Dict],
		indexes_and_sections: Dict[int, SectionStruct]) -> None:

	indexes_and_created: Dict[int, SectionStruct]
	indexes_and_created = {}

	for s in new_elements:
		sn = SectionNew(course=course, **s)
		new_instance = _add_section(sn)
		indexes_and_created[sn.index] = new_instance

	sections: List[SectionStruct | None]
	sections = [None] * (len(indexes_and_sections) + len(indexes_and_created))

	pos = 0

	for i in range(len(sections)):
		if i in indexes_and_created:
			sections[i] = indexes_and_created[i]
			continue

		sections[i] = indexes_and_sections[pos]
		pos += 1

	for i in range(len(sections)):
		indexes_and_sections[i] = sections[i]


def _add_section(section_new: SectionNew) -> SectionStruct:
	s = SectionStruct(
		pk=None,
		name=section_new.name,
		parent_index=section_new.parent,
	)

	return s


def validate_sections(
		indexes_and_sections: Dict[int, SectionStruct],
		pages: Iterable[PageStruct],
		raise_exception=False) -> bool:

	validations = [
		check_sections_not_looped(indexes_and_sections),
		check_sections_only_for_pages_or_only_for_sections(indexes_and_sections.values(), pages)
	]

	if all(validations):
		return True

	if raise_exception:
		raise ValueError() # Sections are not valid

	return False


def check_sections_not_looped(indexes_and_sections: Dict[int, SectionStruct]) -> bool:
	for i, section in indexes_and_sections.items():
		if section.parent_index is None:
			continue

		if section.parent_index in indexes_and_sections:
			continue

		if 0 <= section.parent_index < i:
			continue

		return False

	return True


def check_sections_only_for_pages_or_only_for_sections(
		sections: Iterable[SectionStruct],
		pages: Iterable[PageStruct]) -> bool:

	sections_with_pages = {p.section_index for p in pages}

	for section in sections:
		if section.parent_index in sections_with_pages:
			return False

	return True
