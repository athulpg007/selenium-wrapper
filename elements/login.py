"""Elements used in test_login.py."""

from selenium_wrapper.locate_by import Element

username = Element("username").by_id()
password = Element("password").by_id()
submit = Element("submit").by_id()

elements = [
	username,
	password,
	submit,
]

logout = Element("Log out").by_text_contains()
