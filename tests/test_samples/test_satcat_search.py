from elements import satcat
from elements.satcat import dynamic_search_result


class TestSearchWithDropdown:
	def test_search_with_dropdown(self, browser):
		browser.navigate("https://www.satcat.com/")
		browser.wait_for_element(satcat.search_input)
		norad_id: str = "27386"
		browser.search_with_dropdown(satcat.search_input, norad_id, dynamic_search_result(norad_id))
		browser.wait_for_element(satcat.cds_tabs_list)
		assert "sats/27386" in browser.driver.current_url
