"""Elements used in test_file_download.py."""

from selenium_wrapper.locate_by import Element

download_icon = Element("download-button").by_cls_contains()
download_btn = Element("?download").by_href_contains()
