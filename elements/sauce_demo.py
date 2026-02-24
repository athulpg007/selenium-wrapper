"""Elements used in test_sauce_demo.py."""

from selenium_wrapper.locate_by import Element

username = Element("user-name").by_id()
password = Element("password").by_id()
login_button = Element("login-button").by_id()

login_elements = [username, password, login_button]

login_error_button = Element("error-button").by_cls()
login_error_message = Element(
	"Epic sadface: Username and password do not match any user in this service"
).by_text_contains()

inventory_container = Element("inventory_container").by_id()

add_to_cart_backpack = Element("add-to-cart-sauce-labs-backpack").by_id()
cart_badge = Element("shopping_cart_badge").by_cls()
