"""Implements the tests at https://practicetestautomation.com/practice-test-login/"""

from elements import login


class TestLogin:
	def test_login(self, browser):
		browser.navigate("https://practicetestautomation.com/practice-test-login/")
		browser.input_text(login.username, "student")
		browser.input_text(login.password, "Password123")
		browser.click(login.submit)
		browser.wait_for_element(login.logout)
