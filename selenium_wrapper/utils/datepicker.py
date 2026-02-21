"""Utility class for interacting with date pickers in Selenium tests."""

from selenium_wrapper.locate_by import Element
from selenium_wrapper.utils.timedif import TimeDif


class DatePicker:
	"""Utility class for interacting with date pickers in Selenium tests."""

	def __init__(self) -> None:
		"""Initialize the DatePicker with locators for its elements."""
		self.open = Element("//*[contains(@class, 'open')]").by_xpath()
		self.next_month = Element(
			"//*[contains(@class, 'open')]//span[contains(@class, 'flatpickr-next-month')]"
		).by_xpath()
		self.prev_month = Element(
			"//*[contains(@class, 'open')]//span[contains(@class, 'flatpickr-prev-month')]"
		).by_xpath()

		self.hour_element = Element('//*[contains(@class, "open")]//*[contains(@class,"flatpickr-hour")]').by_xpath()
		self.minute_element = Element(
			'//*[contains(@class, "open")]//*[contains(@class,"flatpickr-minute")]'
		).by_xpath()
		self.second_element = Element(
			'//*[contains(@class, "open")]//*[contains(@class,"flatpickr-second")]'
		).by_xpath()

	@staticmethod
	def int_parse_timestamp(timestamp: str) -> tuple[int, int, int, int, int, int]:
		"""Parse an ISO 8601 timestamp into its integer components.

		:param timestamp: str: The timestamp in ISO 8601 format %Y-%m-%dT%H:%M:%SZ.
		"""
		# check the timestamp format is correct
		assert isinstance(timestamp, str), "Must be a string"
		assert len(timestamp) == 20, "Timestamp must be in ISO 8601 format %Y-%m-%dT%H:%M:%SZ"

		# remove the trailing 'Z'
		timestamp = timestamp.rstrip("Z")
		date_part, time_part = timestamp.split("T")
		year, month, day = map(int, date_part.split("-"))
		hour, minute, second = map(int, time_part.split(":"))
		return year, month, day, hour, minute, second

	@staticmethod
	def get_current_local_time() -> str:
		"""Get the current local time in ISO 8601 format %Y-%m-%dT%H:%M:%SZ."""
		utc_dt = TimeDif().now  # get current UTC datetime
		local_dt = utc_dt.astimezone()  # convert to local timezone
		return local_dt.strftime(format="%Y-%m-%dT%H:%M:%SZ")  # Get ISO string in local time

	def get_month_difference(self, current_time: str, timestamp: str) -> int:
		"""Compute the difference in months between the provided timestamp and the current local time.

		:param current_time: str: The current local time in ISO 8601 format %Y-%m-%dT%H:%M:%SZ.
		:param timestamp: str: The timestamp in ISO 8601 format %Y-%m-%dT%H:%M:%SZ.
		:return: int: the difference in months

		+ve integer if the provided month/year is in the future,
		-ve integer if in the past,
		0 if the same month/year.
		"""
		current_year, current_month, *_ = self.int_parse_timestamp(current_time)
		provided_year, provided_month, *_ = self.int_parse_timestamp(timestamp)
		return (provided_year - current_year) * 12 + (provided_month - current_month)

	@staticmethod
	def select_date(day: int) -> tuple[str, str]:
		"""Return an Element representing the day to be picked in the date picker.

		:param day: int: The day of the month to pick.
		:return: Element: The Element locator for the specified day.
		"""
		return Element(
			f'//*[contains(@class, "open")]'
			f'//*[contains(@class, "flatpickr-day")'
			f' and not(contains(@class, "Month"))'
			f' and text()="{day}"]'
		).by_xpath()
