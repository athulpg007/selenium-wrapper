import pytest

from selenium_wrapper.utils.datepicker import DatePicker


class TestDatePickerIntParseTimestamp:
	"""
	Unit tests for the int_parse_timestamp method of the DatePicker class.
	These tests cover various scenarios including valid timestamps, edge cases,
	and invalid formats.
	"""

	dp = DatePicker()

	def test_valid_timestamp_01(self):
		result = self.dp.int_parse_timestamp("2025-12-31T23:59:59Z")
		assert result == (2025, 12, 31, 23, 59, 59)

	def test_valid_timestamp_02(self):
		result = self.dp.int_parse_timestamp("2000-01-01T00:00:00Z")
		assert result == (2000, 1, 1, 0, 0, 0)

	def test_valid_timestamp_03(self):
		result = self.dp.int_parse_timestamp("1999-07-15T12:30:45Z")
		assert result == (1999, 7, 15, 12, 30, 45)

	def test_edge_case_leap_year(self):
		result = self.dp.int_parse_timestamp("2020-02-29T10:20:30Z")
		assert result == (2020, 2, 29, 10, 20, 30)

	def test_invalid_format_missing_z(self):
		with pytest.raises(AssertionError, match="Timestamp must be in ISO 8601 format %Y-%m-%dT%H:%M:%SZ"):
			self.dp.int_parse_timestamp("2025-12-31T23:59:59")

	def test_invalid_format_wrong_length(self):
		with pytest.raises(AssertionError, match="Timestamp must be in ISO 8601 format %Y-%m-%dT%H:%M:%SZ"):
			self.dp.int_parse_timestamp("2025-12-31T23:59Z")

	def test_invalid_format_non_string(self):
		with pytest.raises(AssertionError, match="Must be a string"):
			self.dp.int_parse_timestamp(20251231235959)


class TestDatePickerMonthDifference:
	"""
	Unit tests for the get_month_difference method of the DatePicker class.
	These tests cover various scenarios including same month, month transitions,
	year transitions, and arbitrary date differences.
	"""

	dp = DatePicker()

	def test_same_month_01(self):
		diff = self.dp.get_month_difference("2025-12-31T00:01:01Z", "2025-12-31T01:01:01Z")
		assert diff == 0

	def test_same_month_02(self):
		diff = self.dp.get_month_difference("2025-06-01T00:01:01Z", "2025-06-30T23:59:59Z")
		assert diff == 0

	def test_one_month_forward(self):
		diff = self.dp.get_month_difference("2025-11-30T00:01:01Z", "2025-12-31T01:01:01Z")
		assert diff == 1

	def test_one_month_backward(self):
		diff = self.dp.get_month_difference("2025-12-31T00:01:01Z", "2025-11-30T01:01:01Z")
		assert diff == -1

	def test_one_year_forward(self):
		diff = self.dp.get_month_difference("2024-06-15T00:01:01Z", "2025-06-15T00:01:01Z")
		assert diff == 12

	def test_one_year_backward(self):
		diff = self.dp.get_month_difference("2025-06-15T00:01:01Z", "2024-06-15T00:01:01Z")
		assert diff == -12

	def test_same_month_day_boundary_forward(self):
		diff = self.dp.get_month_difference("2025-01-01T23:59:59Z", "2025-01-02T00:00:00Z")
		assert diff == 0

	def test_same_month_day_boundary_backward(self):
		diff = self.dp.get_month_difference("2025-01-02T00:00:00Z", "2025-01-01T23:59:59Z")
		assert diff == 0

	def test_end_of_month_forward(self):
		diff = self.dp.get_month_difference("2025-01-31T23:59:00Z", "2025-02-01T00:01:00Z")
		assert diff == 1

	def test_end_of_month_backward(self):
		diff = self.dp.get_month_difference("2025-02-01T00:01:00Z", "2025-01-31T23:59:00Z")
		assert diff == -1

	def test_end_of_year_forward(self):
		diff = self.dp.get_month_difference("2025-12-31T23:59:59Z", "2026-01-01T00:00:00Z")
		assert diff == 1

	def test_end_of_year_backward(self):
		diff = self.dp.get_month_difference("2026-01-01T00:00:00Z", "2025-12-31T23:59:59Z")
		assert diff == -1

	def test_multiple_years_forward(self):
		diff = self.dp.get_month_difference("2020-01-01T00:01:01Z", "2025-01-01T00:01:01Z")
		assert diff == 60

	def test_multiple_years_backward(self):
		diff = self.dp.get_month_difference("2025-01-01T00:01:01Z", "2020-01-01T00:01:01Z")
		assert diff == -60

	def test_arbitrary_dates_forward(self):
		diff = self.dp.get_month_difference("2023-03-15T12:00:00Z", "2025-07-20T15:30:00Z")
		assert diff == 28

	def test_arbitrary_dates_backward(self):
		diff = self.dp.get_month_difference("2025-07-20T15:30:00Z", "2023-03-15T12:00:00Z")
		assert diff == -28

	def test_invalid_date_format(self):
		with pytest.raises(AssertionError, match="Timestamp must be in ISO 8601 format %Y-%m-%dT%H:%M:%SZ"):
			self.dp.get_month_difference("2025/12/31 00:01:01", "2025-11-30T01:01:01Z")
