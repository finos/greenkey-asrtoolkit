#!/usr/bin/env python
"""
Simple wrapper for validating script inputs
"""

from os.path import isfile

from asrtoolkit.file_utils.name_cleaners import get_extension

VALID_EXTENSIONS = ["json", "srt", "stm", "vtt", "txt", "html"]


def valid_input_file(file_name, valid_extensions=[]):
    """
    tests that a file exists and that the extension is one asrtoolkit scripts can accept
    >>> import os
    >>> module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    >>> valid_input_file(f"{module_path}/pyproject.toml")
    False
    >>> valid_input_file(f"{module_path}/pyproject.toml", ["toml"])
    True
    """
    return isfile(file_name) and get_extension(file_name) in (
        valid_extensions if valid_extensions else VALID_EXTENSIONS
    )


def assign_if_valid(file_name, file_format=None):
    from asrtoolkit.data_structures import Transcript

    "returns a time_aligned_text object if valid else None"
    return Transcript(file_name, file_format) if valid_input_file(file_name) else None
