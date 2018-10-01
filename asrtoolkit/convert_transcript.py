#!/usr/bin/env python
"""
Python class for converting file formats used in Automatic Speech Recognition
"""

import argparse

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text


def main():
  parser = argparse.ArgumentParser(description='convert between text file formats')
  parser.add_argument('input_file', metavar='input_file', type=str, help='input file')
  parser.add_argument('output_file', metavar='output_file', type=str, help='output file')
  args = parser.parse_args()

  input_file = time_aligned_text(args.input_file)
  input_file.write(args.output_file)


if __name__ == "__main__":
  main()
