"""
Module with helper class to deal with timestamps.
"""

import datetime


class TimeDif:
	"""
	Helper class to generate ISO formatted time strings with offsets from now.
	"""

	def __init__(
		self,
		day_offset: float | None = None,
		hour_offset: float | None = None,
		minute_offset: float | None = None,
		second_offset: float | None = None,
		microsecond_offset: int | None = None,
		timestamp: str | None = None,
	) -> None:
		"""
		if timestamp is provided, it will be parsed and used as the base time.
		Otherwise, the current UTC time will be used as base time.
		Offsets can be provided to adjust the time from the base time.

		:param day_offset:
		:param hour_offset:
		:param minute_offset:
		:param second_offset:
		:param microsecond_offset: Optional[int]
		:param timestamp: Optional[str]
		"""

		if not timestamp:
			self.now = datetime.datetime.now(datetime.UTC)
		else:
			self.now = self.parse_timestamp(timestamp)

		if day_offset:
			self.now += datetime.timedelta(days=day_offset)
		if hour_offset:
			self.now += datetime.timedelta(hours=hour_offset)
		if minute_offset:
			self.now += datetime.timedelta(minutes=minute_offset)
		if second_offset:
			self.now += datetime.timedelta(seconds=second_offset)
		if microsecond_offset:
			self.now += datetime.timedelta(microseconds=microsecond_offset)

	def iso(self, microseconds: bool = False) -> str:
		"""
		Return the time as ISO formatted string.
		"""
		if microseconds:
			return self.now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		return self.now.strftime("%Y-%m-%dT%H:%M:%SZ")

	def date(self) -> str:
		"""
		Return the date part of the time as a string.
		"""
		return self.now.strftime("%Y-%m-%d")

	@staticmethod
	def parse_timestamp(timestamp: str) -> datetime.datetime:
		"""
		Converts a datetime string in valid format to a datetime object.
		"""
		formats = [
			"%Y-%m-%dT%H:%M:%S.%fZ",  # Format with microseconds and timezone
			"%Y-%m-%dT%H:%M:%SZ",  # Format without microseconds and timezone
			"%Y-%m-%dT%H:%M:%S",  # Format without microseconds or timezone
			"%Y-%m-%dT%H:%M:%S.%f+00:00",  # Format with microseconds and timezone
			"%Y-%m-%dT%H:%M:%S+00:00",  # Format without microseconds
			"%Y-%m-%dT%H:%M:%S.%f",  # Format without timezone
			"%Y-%m-%d %H:%M:%S",  # Format with space, without microseconds, without timezone
		]
		for fmt in formats:
			try:
				dt = datetime.datetime.strptime(timestamp, fmt)
				return dt.replace(tzinfo=datetime.UTC)
			except ValueError:
				continue
		raise ValueError(f"Could not parse timestamp, format: {timestamp}")
