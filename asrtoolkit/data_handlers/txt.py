#!/usr/bin/env python
"""
Module for reading TXT files

This expects a segment from class derived in convert_text
"""

# do not delete - needed in time_aligned_text
from asrtoolkit.data_handlers.data_handlers_common import footer, header, separator
from asrtoolkit.data_structures.segment import segment


def format_segment(seg):
    """
    Formats a segment assuming it's an instance of class segment with text element
    """
    return seg.formatted_text if getattr(seg, "formatted_text") else seg.text


def read_in_memory(input_data):
    """
    Reads input text
    """
    segments = []
    for line in input_data.splitlines():
        segments.append(segment({"text": line.strip()}))
    return segments


def read_file(file_name):
    """
    Reads a TXT file
    """
    segments = []
    with open(file_name, encoding="utf-8") as f:
        segments = read_in_memory(f.read())
    return segments
