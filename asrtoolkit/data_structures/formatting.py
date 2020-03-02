#!/usr/bin/env python3
"""
Holds all formatting utilities
"""


def std_float(number, num_decimals=2):
    """
    Print a number to string with n digits after the decimal point
    (default = 2)
    """
    return "{0:.{1:}f}".format(float(number), num_decimals)


def timestamp_to_seconds(timestamp):
    """
    Convert a timestamp to seconds
    """
    parts = timestamp.split(":")
    return std_float(
        float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2]), 3)


def seconds_to_timestamp(seconds):
    """
    Convert from seconds to a timestamp
    """
    minutes, seconds = divmod(float(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return "%02d:%02d:%06.3f" % (hours, minutes, seconds)


def clean_float(input_float):
    """
    Return float in seconds (even if it was a timestamp originally)
    """
    return (timestamp_to_seconds(input_float)
            if ":" in str(input_float) else std_float(input_float))
