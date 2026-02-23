import logging

from elements import practice_test_automation


class TestReadTable:
	def test_read_table_lang_filter_java(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.click(practice_test_automation.lang_java)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		for k, v in result.items():
			logging.info(f"{k}: {v}")
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
		result = browser.read_table(practice_test_automation.table)
		assert set(result["Language"]) == {"Python"}
		assert set(result["Level"]) == {"Beginner"}
		for enrollment in result["Enrollments"]:
			assert int(enrollment) >= 10000

	def test_read_table_no_results(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		# a combination of filters that results in no courses found
		browser.click(practice_test_automation.lang_python)
		browser.click(practice_test_automation.level_beginner)
		browser.wait_for_element(practice_test_automation.no_results)
		text = browser.get_element_text(practice_test_automation.no_results)
		assert text == "No matching courses."

	def test_read_table_reset_filters(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.click(practice_test_automation.lang_python)
		browser.wait_for_element(practice_test_automation.reset_filters)
		browser.click(practice_test_automation.reset_filters)
		browser.wait_for_element(practice_test_automation.table)

	def test_read_table_sort_enrollment(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.use_dropdown(practice_test_automation.sort_dropdown, practice_test_automation.sort_enrollment)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		enrollments = [int(e) for e in result["Enrollments"]]
		assert enrollments == sorted(enrollments)

	def test_read_table_sort_course_name(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.use_dropdown(practice_test_automation.sort_dropdown, practice_test_automation.sort_course_name)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		course_names = result["Course Name"]
		assert course_names == sorted(course_names)

	def test_read_table_sort_language(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-table/")
		browser.use_dropdown(practice_test_automation.sort_dropdown, practice_test_automation.sort_language)
		browser.wait_for_element(practice_test_automation.table)
		result = browser.read_table(practice_test_automation.table)
		languages = result["Language"]
		assert languages == sorted(languages)
