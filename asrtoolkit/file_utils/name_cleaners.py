#!/usr/bin/env python
"""
Simple wrapper for name-cleaning functions
"""


def basename(file_name):
  """
    Returns basename of a file without the preceding directory
  """
  return file_name.split("/")[-1]


def sanitize_hyphens(file_name):
  """
    Replace hyphens with underscores if present in file name
  """
  if "-" in file_name.split("/")[-1]:
    print(
      "Replacing hyphens with underscores in SPH file output - "
      "check to make sure your audio files and transcript files match"
    )
    file_name = "/".join(file_name.split("/")[:-1]) + file_name.split("/")[-1].replace("-", "_")
  return file_name
