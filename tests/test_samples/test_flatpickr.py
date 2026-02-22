import pytest
import time

from selenium_wrapper.selenium import Selenium
from selenium_wrapper.utils.timedif import TimeDif

from elements.flatpickr import datetimepicker


class TestFlatPickr:
    @pytest.mark.parametrize(
        "timestamp", [TimeDif().iso(), TimeDif(day_offset=30).iso()], ids=["now", "now+30d"]
    )
    def test_flatpickr(self, timestamp):
        browser = Selenium()
        browser.navigate("https://flatpickr.js.org/examples/#datetime")
        browser.use_datepicker(datetimepicker, timestamp, skip_seconds=True)
        time.sleep(3)



