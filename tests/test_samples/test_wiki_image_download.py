from elements import wikipedia_image


class TestFileDownload:
	def test_file_download(self, browser):
		browser.navigate("https://en.wikipedia.org/wiki/Atmospheric_entry#/media/File:Entry.jpg")
		browser.wait_for_element(wikipedia_image.download_icon)
		browser.use_dropdown(wikipedia_image.download_icon, wikipedia_image.download_btn)
		browser.read_file(pattern="*.jpg", binary=True, timeout=10)
