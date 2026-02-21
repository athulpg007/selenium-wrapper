"""Core Selenium WebDriver wrapper for browser automation.

Provides methods for browser initialization, login, navigation, element interaction.

Supported browsers defined in selenium_wrapper.browsers.Browser enum.
"""

import glob
import logging
import os
import time

from selenium import webdriver
from selenium.common.exceptions import (
	ElementClickInterceptedException,
	StaleElementReferenceException,
	TimeoutException,
	WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import env
from selenium_wrapper.browsers import Browser
from selenium_wrapper.locate_by import Element
from selenium_wrapper.utils import file_paths
from selenium_wrapper.utils.datepicker import DatePicker

logging.basicConfig(level=logging.INFO)


class Selenium:
	"""Selenium WebDriver wrapper that initializes a browser."""

	def __init__(
		self,
		browser: str = Browser.CHROME,
		timeout: float = 30,
		headless: bool = env.HEADLESS,
		user_agent: str = f"custom-user-agent",
		login: bool = True,
	) -> None:
		"""Initialize the Selenium WebDriver with the specified parameters.

		:param browser: str: The browser to use default = Browser.CHROME.
		:param timeout: float: The timeout for WebDriverWait, default = 30.
		:param headless: bool: Whether to run the browser in headless mode, default = env.HEADLESS.
		:param user_agent: str: custom override user-agent
		:param login: bool: Whether to perform login after initialization, default = True.

		Example usage:
		- `browser = Selenium()`
		- `browser = Selenium(browser="firefox", timeout=15)`
		"""
		self.browser = browser
		self.timeout = timeout
		self.headless = headless
		self.user_agent = user_agent

		self.driver = None
		self.wait = None

		self.download_dir = file_paths.download_dir
		self.datepicker = DatePicker()
		self.key_name = "key_name"
		self.console_logs = []

		self.select_browser(browser=browser)
		self.set_window_position()
		self.set_window_size()

		if login:
			self.login()

	def _get_webdriver(self, browser: str) -> webdriver.Remote:
		"""Initialize the WebDriver for the specified browser with appropriate options.

		:param browser: str: The browser to use ("chrome", "firefox", "safari", "edge").
		:raises ValueError: If the browser is not supported.
		"""
		if isinstance(browser, str):
			browser = Browser(browser.lower())

		match browser:
			case Browser.CHROME:
				options = webdriver.ChromeOptions()
				options.add_argument(f"--user-agent={self.user_agent}")
				prefs = {
					"download.default_directory": self.download_dir,
					"download.prompt_for_download": False,
					"download.directory_upgrade": True,
				}
				options.add_argument("--window-size=1280,800")
				options.add_experimental_option("prefs", prefs)
				if self.headless:
					# these are required to run headless inside a docker container
					options.add_argument("--no-sandbox")
					options.add_argument("--headless=new")
					options.add_argument("--disable-dev-shm-usage")
					options.add_argument("--window-size=1920,1080")
				return webdriver.Chrome(options=options)
			case Browser.FIREFOX:
				options = webdriver.FirefoxOptions()
				options.set_preference("general.useragent.override", f"{self.user_agent}")
				options.set_preference("browser.download.folderList", 2)
				options.set_preference("browser.download.dir", self.download_dir)
				options.set_preference("browser.download.useDownloadDir", True)
				options.set_preference(
					"browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/octet-stream"
				)
				options.set_preference("pdfjs.disabled", True)  # Disable built-in PDF viewer
				return webdriver.Firefox(options=options)
			case Browser.SAFARI:
				# Safari does not support setting user agent via options
				return webdriver.Safari()
			case Browser.EDGE:
				options = webdriver.EdgeOptions()
				options.add_argument(f"--user-agent={self.user_agent}")
				prefs = {
					"download.default_directory": self.download_dir,
					"download.prompt_for_download": False,
					"download.directory_upgrade": True,
				}
				options.add_experimental_option("prefs", prefs)
				return webdriver.Edge(options=options)
			case _:
				raise ValueError(f"not a valid choice for browser: {browser}")

	def select_browser(self, browser: str) -> None:
		"""Select and initializes the WebDriver for the specified browser.

		:param browser: str: The browser to use ("chrome", "firefox", "safari", or "edge").
		"""
		self.driver = self._get_webdriver(browser=browser)
		self.wait = WebDriverWait(self.driver, self.timeout)

	def set_window_position(self, x: int = 0, y: int = 0) -> None:
		"""Set the position of the browser window.

		:param x: int
		:param y: int
		"""
		self.driver.set_window_position(x, y)

	def set_window_size(self, width: int = 1280, height: int = 800) -> None:
		"""Set the size of the browser window.

		:param width: int
		:param height: int
		"""
		self.driver.set_window_size(width, height)

	def navigate(self, url: str) -> None:
		"""Navigate the browser to the specified URL.

		:param url: str
		"""
		self.driver.get(url)

	def wait_for_element(self, locator: tuple[str, str]) -> WebElement:
		"""Wait for an element to be present on the page.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		:return: WebElement, if found within the timeout period.
		:raises AssertionError: if the element is not found within the timeout period.
		"""
		try:
			return self.wait.until(ec.presence_of_element_located(locator))
		except TimeoutException as e:
			raise AssertionError(
				f"Could not find element By.{locator[0]}='{locator[1]}' after waiting {self.timeout} seconds.\n"
				f"Current URL: {self.driver.current_url}"
			) from e

	def wait_for_element_clickable(self, locator: tuple[str, str]) -> WebElement:
		"""Wait for an element to be clickable on the page.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		:return: WebElement, if found within the timeout period.
		:raises AssertionError: If the element is not clickable within the timeout period.
		"""
		try:
			return self.wait.until(ec.element_to_be_clickable(locator))
		except TimeoutException as e:
			raise AssertionError(
				f"Could not find clickable element By.{locator[0]}='{locator[1]}' waited {self.timeout} seconds.\n"
				f"Current URL: {self.driver.current_url}"
			) from e

	def wait_for_element_invisible(self, locator: tuple[str, str]) -> bool:
		"""Wait for an element to become invisible on the page.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		:return: bool, True if the element becomes invisible within the timeout period.
		:raises AssertionError: If the element does not become invisible within the timeout period.
		"""
		try:
			return self.wait.until(ec.invisibility_of_element_located(locator))
		except TimeoutException as e:
			raise AssertionError(
				f"Element By.{locator[0]}='{locator[1]}' did not become invisible, waited {self.timeout} seconds.\n"
				f"Current URL: {self.driver.current_url}"
			) from e

	def click(self, locator: tuple[str, str]) -> None:
		"""Wait for an element to be clickable and clicks it.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		"""
		try:
			element = self.wait_for_element_clickable(locator)
			element.click()
		except (ElementClickInterceptedException, StaleElementReferenceException):
			# Retry once if common click exceptions occur
			time.sleep(0.5)
			element = self.wait_for_element_clickable(locator)
			element.click()

	def input_text(self, locator: tuple[str, str], text: str | float) -> None:
		"""Wait for an element to be clickable, clears it, and inputs text.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		:param text: str | float: The text to input into the element.
		"""
		element = self.wait_for_element_clickable(locator)
		element.clear()
		element.send_keys(text)

	def search_with_dropdown(self, locator: tuple[str, str], value: str, choice: tuple[str, str]) -> None:
		"""Input text into a search field and selects a choice from the dropdown.

		:param locator: tuple[str, str]: locator for the search input field
		:param value: str: text to input into the search field
		:param choice: tuple[str, str]: locator for the choice to select from the dropdown
		"""
		self.input_text(locator, value)
		try:
			self.click(choice)
		except AssertionError:
			logging.info("Retrying to click search dropdown choice ...")
			self.input_text(locator, value)
			self.click(choice)

	def get_element_text(self, locator: tuple[str, str]) -> str:
		"""Wait for an element to be present and returns its text.

		:param locator: tuple[str, str]: A tuple containing the locator strategy and locator value.
		:return: str: The text of the element if found.
		:raises AssertionError: If the element is not present within the timeout period.
		"""
		try:
			element = self.wait_for_element(locator)
			return element.text
		except Exception as e:
			raise AssertionError(f"Could not get text of element By.{locator[0]}='{locator[1]}': {e}") from e

	def use_dropdown(self, dropdown: tuple[str, str], choice: tuple[str, str], delay: float = 0.5) -> None:
		"""Use a dropdown to select the specified option.

		:param dropdown: tuple[str, str]: Locator for the dropdown element.
		:param choice: tuple[str, str]: Locator for choice to select from the dropdown.
		:param delay: float: Time to wait after clicking dropdown before selecting choice.
		"""
		self.click(dropdown)
		time.sleep(delay)  # wait for dropdown options to appear
		self.click(choice)

	def press_key(self, key: str) -> None:
		"""Presses a key using ActionChains.

		:param key: The key to press (e.g., Keys.ENTER, Keys.ESCAPE).
		"""
		action = ActionChains(self.driver)
		action.send_keys(key)
		action.perform()

	def use_datepicker(self, datepicker: tuple[str, str], timestamp: str, delay: float = 0.5) -> None:
		"""Use a date picker to select the date and time from a timestamp.

		:param datepicker: tuple[str, str]: Locator for the date picker input field.
		:param timestamp: str: The timestamp in ISO 8601 format %Y-%m-%dT%H:%M:%SZ.
		:param delay: float, default=0.5
		"""
		# open the datepicker
		self.click(datepicker)

		# ensure datepicker is open
		calendar = self.datepicker.open
		try:
			self.wait_for_element(calendar)
		except AssertionError as e:
			raise AssertionError("Date picker is not open. Cannot continue.") from e

		# Parse date and time integer components from the timestamp
		parsed = self.datepicker.int_parse_timestamp(timestamp)
		provided_year, provided_month, provided_day = parsed[:3]
		provided_hour, provided_min, provided_sec = parsed[3:6]

		# Compute month difference wrt current local time
		current_time: str = self.datepicker.get_current_local_time()
		month_diff: int = self.datepicker.get_month_difference(current_time, timestamp)

		# Navigate to correct month if month_diff != 0
		if month_diff > 0:
			for _ in range(month_diff):
				self.click(self.datepicker.next_month)
		elif month_diff < 0:
			for _ in range(abs(month_diff)):
				self.click(self.datepicker.prev_month)
		# else month_diff == 0, do nothing - already on correct month

		# pick the day
		day_element = self.datepicker.select_date(provided_day)
		self.click(day_element)

		# pick the time
		self.input_text(self.datepicker.hour_element, provided_hour)
		self.input_text(self.datepicker.minute_element, provided_min)
		self.input_text(self.datepicker.second_element, provided_sec)

		# close the datepicker
		self.press_key(Keys.ESCAPE)
		time.sleep(delay)  # wait before moving on

	def download_with_key(self, locator: tuple[str, str], delay: float = 0.5) -> None:
		"""Clicks the primary download button and then the API key download button.

		:param locator: tuple[str, str]: Locator for the primary download button.
		:param delay: float: Time to wait after clicking primary download before selecting key option.
		"""
		self.click(locator)
		secondary_locator = Element(f"{locator[1]}//*[contains(text(), '{self.key_name}')]").by_xpath()
		time.sleep(delay)  # wait for secondary download options to appear
		self.click(secondary_locator)

	def get_filename_matching_pattern(self, pattern: str, timeout: int = 30, poll_interval: float = 0.5) -> str | None:
		"""Poll until it's found or timeout is reached, then returns the first filename matching the pattern.

		:param pattern: str: The pattern to match filenames against using glob.glob().
		:param timeout: int: Maximum time to wait for the file in seconds.
		:param poll_interval: float: Time interval between each check in seconds.
		:return: str: The filename if found.
		:raises FileNotFoundError: If no matching file is found within the timeout period
		"""
		start_time = time.time()
		while time.time() - start_time <= timeout:
			matching_file = glob.glob(f"{self.download_dir}/{pattern}")
			if matching_file:
				logging.info(f"Found matching file: {matching_file}")
				return matching_file[0].split("/")[-1]  # extract filename from full path
			time.sleep(poll_interval)
		raise FileNotFoundError(f"File matching pattern '{pattern}' not found after {timeout} seconds")

	def read_file(
		self,
		file_path: str = None,
		pattern: str = None,
		timeout: int = 30,
		poll_interval: float = 0.5,
		binary: bool = False,
	) -> str | bytes | None:
		"""Poll for the file until it's found or timeout is reached, then reads and returns its content.

		:param file_path: Relative path to the file within the download directory.
		:param pattern: Pattern to match filenames within the download directory.
		:param timeout: Maximum time to wait, default = 30 seconds.
		:param poll_interval: Time interval between each check in seconds.
		:param binary: Whether to read the file in binary mode.
		:return: Content of the file as a string or bytes, or None if not found.
		:raises ValueError: If neither file_path nor pattern is provided.
		:raises FileNotFoundError: If the file is not found within the timeout period
		"""
		if file_path:
			full_path = f"{self.download_dir}/{file_path}"
		elif pattern:
			filename = self.get_filename_matching_pattern(pattern=pattern, timeout=timeout, poll_interval=poll_interval)
			full_path = f"{self.download_dir}/{filename}"
		else:
			raise ValueError("Either file_path or pattern must be provided.")
		start_time = time.time()
		while not os.path.exists(full_path):
			if time.time() - start_time > timeout:
				raise FileNotFoundError(f"File not found after {timeout} seconds: {full_path}")
			time.sleep(poll_interval)

		try:
			mode = "rb" if binary else "r"
			with open(full_path, mode) as file:
				return file.read()
		except Exception as e:
			logging.error(f"Error reading file {full_path}: {e}")
			return None

	def login(self, delay: float = 1.0) -> None:
		"""Login to the application.

		:param delay: float: Delay between actions to avoid click Exceptions, default = 1.0.
		"""
		pass

	def logout(self, delay: float = 1.0) -> None:
		"""Log out of the application.

		:param delay: float: Delay between actions to avoid click Exceptions, default = 1.0.
		"""
		pass

	def switch_to_tab(self, tab_index: int = 1) -> None:
		"""Switch focus to a new tab.

		:param tab_index: int, index of the tab to switch to (0-based). defaults to 1 (second tab).
		"""
		try:
			self.driver.switch_to.window(self.driver.window_handles[tab_index])
		except IndexError as e:
			raise AssertionError(
				f"Cannot switch to tab index {tab_index}: only {len(self.driver.window_handles)} tabs open."
			) from e

	def get_browser_console_logs(self) -> None:
		"""Fetch browser console logs and store them in self.console_logs.

		Only works for Google Chrome browser.
		"""
		if self.browser != Browser.CHROME or self.driver is None:
			return
		try:
			self.console_logs = self.driver.get_log("browser")
		except Exception as e:
			logging.error(f"Error fetching browser logs: {e}")

	def print_browser_console_logs(self) -> None:
		"""Print the stored browser console logs for debugging in case of failure."""
		self.get_browser_console_logs()
		if not self.console_logs:
			return
		logging.info("Browser console logs:")
		logging.info("--------------------------------------------------------------------------------")
		for entry in self.console_logs:
			logging.info(f"entry = {entry}")
			logging.info("--------------------------------------------------------------------------------")

	def __del__(self) -> None:
		"""Quit the WebDriver when the Selenium object is deleted.

		Ensures that the browser is closed properly, and resources are released.
		"""
		if hasattr(self, "driver") and self.driver is not None:
			try:
				self.driver.quit()
			except WebDriverException as e:
				logging.error(f"Error quitting WebDriver: {e}")
