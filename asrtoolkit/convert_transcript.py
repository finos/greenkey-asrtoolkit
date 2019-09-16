#!/usr/bin/env python
"""
Python class for converting file formats used in Automatic Speech Recognition
"""

import argparse
import sys
import logging
from asrtoolkit.file_utils.script_input_validation import assign_if_valid
LOGGER = logging.getLogger(__name__)


def check_input_file_validity(input_file):
    if input_file is None:
        LOGGER.error("Invalid input file {}".format(input_file))
        sys.exit(1)


def convert(input_file, output_file):
    input_file = assign_if_valid(input_file)
    input_file.write(output_file)


def main():
    parser = argparse.ArgumentParser(
        description='convert between text file formats')
    parser.add_argument('input_file',
                        metavar='input_file',
                        type=str,
                        help='input file')
    parser.add_argument('output_file',
                        metavar='output_file',
                        type=str,
                        help='output file')
    args = parser.parse_args()

    check_input_file_validity(args.input_file)

    convert(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
