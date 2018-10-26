#!/usr/bin/env python
"""
Simple wrapper for general file functions
"""


def make_list_of_dirs(input_dir_list):
  """
    Make an entire list of directories
  """
  import os
  for this_dir in input_dir_list:
    os.makedirs(this_dir, exist_ok=True)
