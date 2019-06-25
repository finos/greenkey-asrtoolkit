#!/usr/bin/env python
"""
Python class for validating STM files used in Automatic Speech Recognition
"""

import argparse

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.script_input_validation import valid_input_file


def main():
  parser = argparse.ArgumentParser(description='convert between text file formats')
  parser.add_argument('input_file', metavar='input_file', type=str, help='input stm file')
  args = parser.parse_args()

  if valid_input_file(args.input_file):
    # after reading in, only valid lines will remain
    input_file = time_aligned_text(args.input_file)
    # write back to original file name
    input_file.write(args.input_file)
  else:
    print("Invalid input file {}".format(args.input_file))
