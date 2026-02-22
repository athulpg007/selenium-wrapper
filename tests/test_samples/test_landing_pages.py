import time

import pytest


class TestLandingPages:
	@pytest.mark.parametrize(
		"url",
		[
			"https://www.amazon.com",
			"https://www.apple.com",
			"https://www.facebook.com",
			"https://www.google.com",
			"https://www.netflix.com",
		],
		ids=[
			"apple.com",
			"amazon.com",
			"facebook.com",
			"google.com",
			"netflix.com",
		],
	)
	def test_landing_page(self, browser, url):
		browser.navigate(url)
		assert url.split("www.")[1] in browser.driver.current_url
		time.sleep(3)
