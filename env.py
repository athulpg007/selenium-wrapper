"""Set the environment variables to use."""

import os

TEMP_FILE_DIR = "./tmp"  # Temporary file directory for downloaded files.


# HEADLESS defaults to False when running locally. Set it to True if you want headless.
HEADLESS = os.environ.get("HEADLESS", "False").lower() == "true"

