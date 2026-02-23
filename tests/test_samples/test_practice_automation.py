from elements import practice_test_automation


class TestReadTable:
	def test_read_table_lang_filter_java(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.click(practice_test_automation.lang_java)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table, debug=True)
		assert set(result["Language"]) == {"Java"}

	def test_read_table_level_filter_beginner(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		# uncheck other levels to filter only beginner
		browser.click(practice_test_automation.level_intermediate)
		browser.click(practice_test_automation.level_advanced)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		assert set(result["Level"]) == {"Beginner"}

	def test_read_table_enrollment_filter_10000(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.use_dropdown(practice_test_automation.enrollment_dropdown, practice_test_automation.choice_10000)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		for enrollment in result["Enrollments"]:
			assert int(enrollment) >= 10000

	def test_read_table_combined_filters(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.click(practice_test_automation.lang_python)
		# uncheck other levels to filter only beginner
		browser.click(practice_test_automation.level_intermediate)
		browser.click(practice_test_automation.level_advanced)
		# select enrollment filter 10000
		browser.use_dropdown(practice_test_automation.enrollment_dropdown, practice_test_automation.choice_10000)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table, debug=True)
		assert set(result["Language"]) == {"Python"}
		assert set(result["Level"]) == {"Beginner"}
		for enrollment in result["Enrollments"]:
			assert int(enrollment) >= 10000
