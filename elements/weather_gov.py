"""Elements for weather.gov."""

from selenium_wrapper.locate_by import Element

search_box = Element("inputstring").by_id()
first_search_result = Element("//*[@data-index='0']").by_xpath()
current_conditions = Element("current-conditions").by_id()
current_location = Element("//*[@id='current-conditions']//*[@class='panel-title']").by_xpath()

current_forecast = Element("myforecast-current").by_cls()
current_temp_f = Element("myforecast-current-lrg").by_cls()
current_temp_c = Element("myforecast-current-sm").by_cls()

current_conditions_detail = Element("current_conditions_detail").by_id()
