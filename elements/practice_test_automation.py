"""Elements used in test_read_table.py."""

from selenium_wrapper.locate_by import Element

lang_any = Element("//*[@value='Any']").by_xpath()
lang_java = Element("//*[@value='Java']").by_xpath()
lang_python = Element("//*[@value='Python']").by_xpath()

level_beginner = Element("//*[@value='Beginner']").by_xpath()
level_intermediate = Element("//*[@value='Intermediate']").by_xpath()
level_advanced = Element("//*[@value='Advanced']").by_xpath()

enrollment_dropdown = Element("dropdown-button").by_cls()
choice_10000 = Element("//*[@data-value='10000']").by_xpath()

sort_dropdown = Element("sortBy").by_id()
sort_enrollment = Element("//*[@value='col_enroll']").by_xpath()
sort_course_name = Element("//*[@value='col_course']").by_xpath()
sort_language = Element("//*[@value='col_lang']").by_xpath()

reset_filters = Element("resetFilters").by_id()

table = Element("courses_table").by_id()
no_results = Element("noData").by_id()
