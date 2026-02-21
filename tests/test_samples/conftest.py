"""Pytest configuration for acceptance tests using Selenium.

- pytest_sessionstart(): Creates temporary download directories before tests run.
- pytest_sessionfinish(): Cleans up temporary download directories after tests complete.
- browser_ fixture: Provides a Selenium browser instance for each test function and prints browser console logs
"""

import os
import shutil
from collections.abc import Generator

import pytest

from selenium_wrapper.selenium import Selenium
from selenium_wrapper.utils.file_paths import download_dir


# at the start of the pytest session, create the tmp download director(ies) if they don't exist
def pytest_sessionstart():
	os.makedirs(download_dir, exist_ok=True)


# at the end of the pytest session, remove the tmp download director(ies) and all its contents
def pytest_sessionfinish():
	shutil.rmtree(download_dir, ignore_errors=True)


# fixture to provide a Selenium browser instance for each test function
# prints browser console logs after the test function completes
# named 'browser_' to avoid conflict with 'browser' parameter in other fixtures
# after all tests are migrated, this can be renamed to 'browser'
@pytest.fixture
def browser_() -> Generator[Selenium, None, None]:
	"""
	Provides a Selenium browser instance for the test.
	"""
	browser = Selenium()
	yield browser
	browser.print_browser_console_logs()
