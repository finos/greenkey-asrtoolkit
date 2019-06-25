#!/usr/bin/env python
"""
Simple wrapper for validating script inputs
"""

from os.path import exists
from asrtoolkit.file_utils.name_cleaners import get_extension

VALID_EXTENSIONS = ["json", "srt", "stm", "vtt", "txt", "html"]


def valid_input_file(file_name, valid_extensions=[]):
  """
  tests that a file exists and that the extension is one asrtoolkit scripts can accept
  >>> valid_input_file("setup.py")
  False
  >>> valid_input_file("setup.py", ["py"])
  True
  >>> valid_input_file("requirements.txt")
  True
  """
  return exists(file_name) and get_extension(file_name) in (valid_extensions if valid_extensions else VALID_EXTENSIONS)