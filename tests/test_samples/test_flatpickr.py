import time

import pytest

from elements.flatpickr import datetimepicker
from selenium_wrapper.utils.timedif import TimeDif


class TestFlatPickr:
	@pytest.mark.parametrize("timestamp", [TimeDif().iso(), TimeDif(day_offset=30).iso()], ids=["now", "now+30d"])
	def test_flatpickr(self, browser, timestamp):
		browser.navigate("https://flatpickr.js.org/examples/#datetime")
		browser.use_datepicker(datetimepicker, timestamp, skip_seconds=True)
		time.sleep(3)
