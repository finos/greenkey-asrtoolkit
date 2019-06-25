#!/usr/bin/env python
"""
Python class for validating STM files used in Automatic Speech Recognition
"""

import argparse

from asrtoolkit.convert_transcript import convert


def validate():
    parser = argparse.ArgumentParser(
        description='convert between text file formats')
    parser.add_argument('input_file',
                        metavar='input_file',
                        type=str,
                        help='input file')
    args = parser.parse_args()

    # after reading in, only valid lines will remain
    # so write it back in place
    convert(args.input_file, args.input_file)


if __name__ == "__main__":
    validate()
