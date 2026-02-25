import logging
import secrets

from elements import weather_gov


class TestWeatherGov:
	def test_weather_gov(self, browser):
		browser.navigate("https://www.weather.gov/")

		zip_codes = [
			"99685",  # Unalaska, AK
			"80112",  # Englewood, CO
			"96753",  # Kahului, HI
			"98101",  # Seattle, WA
			"85003",  # Phoenix, AZ
			"33040",  # Key West, FL
			"04609",  # Bar Harbor, ME
		]
		zip_code = secrets.choice(zip_codes)  # randomly select a zip code for testing

		browser.search_with_dropdown(weather_gov.search_box, zip_code, weather_gov.first_search_result)
		browser.wait_for_element(weather_gov.current_conditions)
		location_text = browser.get_element_text(weather_gov.current_location)
		current_forecast_text = browser.get_element_text(weather_gov.current_forecast)
		current_temp_c_text = browser.get_element_text(weather_gov.current_temp_c)
		current_temp_f_text = browser.get_element_text(weather_gov.current_temp_f)

		current_conditions_table = browser.read_table(weather_gov.current_conditions_detail)

		logging.info("-----------------------------------")
		logging.info("Current location: %s", location_text)
		logging.info("Current forecast: %s", current_forecast_text)
		logging.info("Current temp (F): %s", current_temp_f_text)
		logging.info("Current temp (C): %s", current_temp_c_text)
		logging.info("-----------------------------------")
		logging.info("Current conditions details:")
		for v in current_conditions_table.values():
			logging.info(f"{v[0]}: {v[1]}")
		logging.info("-----------------------------------")
