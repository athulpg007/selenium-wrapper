"""Module defining supported web browsers using an enumeration."""

from enum import Enum


class Browser(Enum):
	"""Enum representing supported web browsers."""

	CHROME = "chrome"
	FIREFOX = "firefox"
	SAFARI = "safari"
	EDGE = "edge"
