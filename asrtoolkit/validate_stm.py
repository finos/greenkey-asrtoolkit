#!/usr/bin/env python
"""
Python class for validating STM files used in Automatic Speech Recognition
"""

import argparse

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text


def main():
  parser = argparse.ArgumentParser(description='convert between text file formats')
  parser.add_argument('input_file', metavar='input_file', type=str, help='input stm file')
  args = parser.parse_args()

  # after reading in, only valid lines will remain
  input_file = time_aligned_text(args.input_file)

  # write back to original file name
  input_file.write(args.input_file)
