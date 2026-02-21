"""Utility functions for managing file paths to tmp download directories."""

import os

from env import TEMP_FILE_DIR

# Get the root directory of selenium-wrapper, two levels up from this file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

PYTEST_XDIST_WORKER = os.environ.get("PYTEST_XDIST_WORKER", "master")

# Define the download directory path, e.g., /tmp
download_dir_root = os.path.join(ROOT_DIR, TEMP_FILE_DIR)
download_dir = os.path.join(download_dir_root, f"{PYTEST_XDIST_WORKER}")
