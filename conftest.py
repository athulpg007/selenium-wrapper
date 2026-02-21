"""root conftest for pytest."""

import os
import sys

"""
Add the project root to sys.path for running pytest in terminal.
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
