#!/usr/bin/env python
"""
Python class for validating STM files used in Automatic Speech Recognition
"""

import argparse

from asrtoolkit.file_utils.script_input_validation import assign_if_valid


def main():
  parser = argparse.ArgumentParser(description='convert between text file formats')
  parser.add_argument('input_file', metavar='input_file', type=str, help='input stm file')
  args = parser.parse_args()

  # after reading in, only valid lines will remain
  input_file = assign_if_valid(args.input_file)
  if input_file is not None:
    # write back to original file name
    input_file.write(args.input_file)
  else:
    print("Invalid input file {}".format(args.input_file))
