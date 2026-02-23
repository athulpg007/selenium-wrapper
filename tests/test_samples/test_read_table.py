import logging

from elements import read_table


class TestReadTable:
	def test_read_table_lang_filter_java(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.click(read_table.lang_java)
		browser.wait_for_element(read_table.table)
		result = browser.read_table(read_table.table)
		logging.info("Read table result:")
		for k, v in result.items():
			logging.info(f"{k}: {v}")
		assert set(result["Language"]) == {"Java"}

	def test_read_table_level_filter_beginner(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		# uncheck other levels to filter only beginner
		browser.click(read_table.level_intermediate)
		browser.click(read_table.level_advanced)
		browser.wait_for_element(read_table.table)
		result = browser.read_table(read_table.table)
		logging.info("Read table result:")
		for k, v in result.items():
			logging.info(f"{k}: {v}")
		assert set(result["Level"]) == {"Beginner"}
