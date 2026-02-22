"""Elements used in test_read_table.py."""

from selenium_wrapper.locate_by import Element

lang_any = Element("//*[@value='Any']").by_xpath()
lang_java = Element("//*[@value='Java']").by_xpath()
lang_python = Element("//*[@value='Python']").by_xpath()

table_rows = Element("//table[@id='myTable']/tbody/tr")
