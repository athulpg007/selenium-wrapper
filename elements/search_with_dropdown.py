"""Elements used in test_search_with_dropdown.py."""

from selenium_wrapper.locate_by import Element

search_input = Element("sat-search").by_id()


def dynamic_search_result(norad_id: str) -> tuple[str, str]:
	"""Return an Element for the search result with the given NORAD ID."""
	return Element(f"/sats/{norad_id}").by_href_contains()


cds_tabs_list = Element("cds--tab--list").by_cls_contains()
