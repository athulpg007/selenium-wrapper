from elements import sauce_demo


class TestSauceDemo:
	def test_login(self, browser):
		browser.navigate("https://www.saucedemo.com/")
		for element in sauce_demo.login_elements:
			browser.wait_for_element(element)
		browser.input_text(sauce_demo.username, "standard_user")
		browser.input_text(sauce_demo.password, "secret_sauce")
		browser.click(sauce_demo.login_button)
		browser.wait_for_element(sauce_demo.inventory_container)

	def test_login_invalid_credentials(self, browser):
		browser.navigate("https://www.saucedemo.com/")
		for element in sauce_demo.login_elements:
			browser.wait_for_element(element)
		browser.input_text(sauce_demo.username, "invalid_user")
		browser.input_text(sauce_demo.password, "invalid_password")
		browser.click(sauce_demo.login_button)
		browser.wait_for_element(sauce_demo.login_error_button)
		browser.wait_for_element(sauce_demo.login_error_message)
