"""Helper for locating elements by different strategies."""

from selenium.webdriver.common.by import By


class Element:
	"""Helper class that provides different strategies for locating elements."""

	def __init__(self, locator: str) -> None:
		"""Locate elements using a locator string, with a specific strategy.

		:param locator: str, The locator string used to find elements.

		Example usage:
		- `element_by_id = Element("element_id").by_id()`
		- `element_by_xpath = Element("//div[@class='example']").by_xpath()`
		"""
		self.locator = locator

	def by_id(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their ID.

		:return: A tuple representing the locator.
		"""
		return By.ID, self.locator

	def by_name(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their name attribute.

		:return: A tuple representing the locator.
		"""
		return By.NAME, self.locator

	def by_xpath(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their XPath.

		:return: A tuple representing the locator.
		"""
		return By.XPATH, self.locator

	def by_cls(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their class name.

		:return: A tuple representing the locator.
		"""
		return By.CLASS_NAME, self.locator

	def by_cls_contains(self) -> tuple[str, str]:
		"""Return a locator that finds elements containing the specified class name.

		:return: A tuple representing the locator.
		"""
		return By.XPATH, f"//*[contains(@class, '{self.locator}')]"

	def by_text(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their exact text.

		:return:
		"""
		return By.XPATH, f"//*[text()='{self.locator}']"

	def by_text_contains(self) -> tuple[str, str]:
		"""Return a locator that finds elements containing the specified text.

		:return:
		"""
		return By.XPATH, f"//*[contains(text(), '{self.locator}')]"

	def by_href(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their exact href attribute.

		:return:
		"""
		return By.XPATH, f"//*[@href='{self.locator}']"

	def by_href_contains(self) -> tuple[str, str]:
		"""Return a locator that finds elements containing the specified href attribute.

		:return:
		"""
		return By.XPATH, f"//*[contains(@href, '{self.locator}')]"

	def by_stripped_text(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their stripped text.

		:return:
		"""
		return By.XPATH, f'//*[normalize-space(text())="{self.locator}"]'

	def by_data_value(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their data-value attribute.

		:return:
		"""
		return By.XPATH, f"//*[@data-value='{self.locator}']"

	def by_data_tab(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their data-tab attribute.

		:return:
		"""
		return By.XPATH, f"//*[@data-tab='{self.locator}']"

	def by_data_tip_contains(self) -> tuple[str, str]:
		"""Return a locator that finds elements containing the specified data-tip attribute.

		:return:
		"""
		return By.XPATH, f"//*[contains(@data-tip, '{self.locator}')]"

	def by_type(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their type attribute.

		:return:
		"""
		return By.XPATH, f"//*[@type='{self.locator}']"

	def by_placeholder(self) -> tuple[str, str]:
		"""Return a locator that finds elements by their placeholder attribute.

		:return:
		"""
		return By.XPATH, f"//*[@placeholder='{self.locator}']"
