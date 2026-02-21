"""
Tests for the Selenium class.
These are intended to run only locally due to the need for various browser drivers.
"""

import time

import pytest

from selenium_wrapper.selenium import Selenium


class TestSelenium:
	@pytest.mark.parametrize("browser", ["chrome", "firefox"])
	def test_selenium_initialization(self, browser):
		"""
		Tests the initialization of the Selenium class with Google Chrome browser.
		:param browser: Selenium instance
		"""
		browser_ = Selenium(browser)
		assert browser_.driver is not None
		browser_.navigate("https://www.selenium.dev")
		time.sleep(3)  # Delay to visually confirm browser opened

	def test_selenium_default_parameters(self):
		"""
		Tests the initialization of the Selenium class with default parameters.
		"""
		browser_ = Selenium()
		assert browser_.driver is not None
		browser_.navigate("https://www.selenium.dev")
		time.sleep(3)  # Delay to visually confirm browser opened

	def test_selenium_invalid_browser(self):
		"""
		Tests the initialization of the Selenium class with an invalid browser.
		"""
		with pytest.raises(ValueError, match="not a valid Browser"):
			Selenium("invalid_browser")
