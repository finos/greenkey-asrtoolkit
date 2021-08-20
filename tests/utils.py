#!/usr/bin/env python3
"""
Helper functions to find the test and sample directories
"""
import os


def get_test_dir(input_file):
    """
    >>> get_test_dir(__file__).endswith("tests")
    True
    """
    return os.path.dirname(os.path.realpath(input_file))


def get_sample_dir(input_file):
    """
    >>> get_sample_dir(__file__).endswith("samples")
    True
    """
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(input_file))), "samples"
    )
