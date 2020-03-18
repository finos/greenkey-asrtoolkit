#!/usr/bin/env python
"""
Python class for validating STM files used in Automatic Speech Recognition
"""

from fire import Fire

from asrtoolkit.convert_transcript import convert


def validate(input_file):
    """
    Overwrites an STM file, leaving only valid input lines
    """

    # after reading in, only valid lines will remain
    # so write it back in place
    convert(input_file, input_file)


def cli():
    Fire(validate)


if __name__ == "__main__":
    cli()
