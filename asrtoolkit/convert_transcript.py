#!/usr/bin/env python
"""
Python class for converting file formats used in Automatic Speech Recognition
"""

import logging
import sys

from fire import Fire

from asrtoolkit.file_utils.script_input_validation import assign_if_valid

LOGGER = logging.getLogger(__name__)


def check_input_file_validity(input_file):
    if input_file is None:
        LOGGER.error("Invalid input file %s", input_file)
        sys.exit(1)


def convert(input_file, output_file, json_format=None):
    """
    Convert between text file formats (supported formats are stm, json, srt, vtt, txt, and html)

    Validates lines of transcript before writing new file.
    STM files are unformatted (eg 10 -> ten)
    """
    check_input_file_validity(input_file)
    input_file = assign_if_valid(
        input_file,
        file_format=(
            json_format if json_format and input_file.endswith(".json") else None
        ),
    )
    input_file.write(
        output_file,
        file_format=json_format
        if json_format and output_file.endswith(".json")
        else None,
    )


def cli():
    Fire(convert)


if __name__ == "__main__":
    cli()
