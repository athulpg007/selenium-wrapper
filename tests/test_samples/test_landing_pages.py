import time

from selenium_wrapper.selenium import Selenium


class TestLandingPages:
    def test_apple_landing_page(self):
        browser = Selenium()
        browser.navigate("https://www.apple.com")
        assert "apple.com" in browser.driver.current_url
        time.sleep(3)

    def test_facebook_landing_page(self):
        browser = Selenium()
        browser.navigate("https://www.facebook.com")
        assert "facebook.com" in browser.driver.current_url
        time.sleep(3)

    def test_google_landing_page(self):
        browser = Selenium()
        browser.navigate("https://www.google.com")
        assert "google.com" in browser.driver.current_url
        time.sleep(3)

    def test_amazon_landing_page(self):
        browser = Selenium()
        browser.navigate("https://www.amazon.com")
        assert "amazon.com" in browser.driver.current_url
        time.sleep(3)


