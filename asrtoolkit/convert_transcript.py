#!/usr/bin/env python
"""
Python class for converting file formats used in Automatic Speech Recognition
"""

import argparse
import logging
from asrtoolkit.file_utils.script_input_validation import assign_if_valid
LOGGER = logging.getLogger(__name__)


def convert():
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

    input_file = assign_if_valid(args.input_file)

    if input_file is not None:
        input_file.write(args.output_file)
    else:
        LOGGER.error("Invalid input file {}".format(args.input_file))


if __name__ == "__main__":
    convert()
