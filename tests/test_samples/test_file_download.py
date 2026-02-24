from elements import file_download


class TestFileDownload:
	def test_file_download(self, browser):
		browser.navigate("https://en.wikipedia.org/wiki/Atmospheric_entry#/media/File:Entry.jpg")
		browser.wait_for_element(file_download.download_icon)
		browser.use_dropdown(file_download.download_icon, file_download.download_btn)
		browser.read_file(pattern="*.jpg", binary=True, timeout=10)
