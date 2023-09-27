from typing import NamedTuple, Optional, Dict, List, Iterable


class PageStruct(NamedTuple):
	pk: Optional[int]
	name: str
	section_index: int
	content: str
	answer: Optional[Dict]


IndexesAndPages = Dict[int, PageStruct]


def delete_pages(indexes_and_pages: IndexesAndPages, delete_indexes_list: List[int]) -> List[PageStruct]:
	delete_indexes = set(delete_indexes_list)
	pages = list[PageStruct]()
	deleted = list[PageStruct]()

	for i in range(len(indexes_and_pages)):
		page = indexes_and_pages[i]

		if i not in delete_indexes:
			pages.append(page)

		deleted.append(page)

	indexes_and_pages.clear()

	for i, page in enumerate(pages):
		indexes_and_pages[i] = page

	return deleted


def edit_pages(indexes_and_pages: IndexesAndPages, edits: List[Dict]):
	new_old_indexes = dict[int, int]()

	for edit in edits:
		index = edit['index']
		page = indexes_and_pages[index]

		_edit_index_independent_fields(page, edit)
		new_index = edit.get('new_index')

		if new_index is not None:
			new_old_indexes[new_index] = index

	_reorder_pages(indexes_and_pages, new_old_indexes)


def _edit_index_independent_fields(page: PageStruct, edit: Dict) -> None:
	pass


def _reorder_pages(indexes_and_pages: IndexesAndPages, new_old_indexes: Dict[int, int]) -> None:
	pass


def add_pages(indexes_and_pages: IndexesAndPages, new_pages: List[Dict]):
	pass


def validate_pages(indexes_and_pages: IndexesAndPages, raise_exception=False) -> bool:
	validations = [
		_check_all_pages_linked_to_sections(indexes_and_pages.values())
	]

	if all(validations):
		return True

	if raise_exception:
		raise ValueError() # pages are not valid

	return False


def _check_all_pages_linked_to_sections(pages: Iterable[PageStruct]) -> bool:
	for p in pages:
		if p.section_index is None:
			return False

	return True
