#!/usr/bin/env python
"""
Module for reading TXT files

This expects a segment from class derived in convert_text
"""

from asrtoolkit.data_structures.segment import segment


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with text element
  """
  return seg.text


def read_file(file_name):
  """
    Reads a TXT file
  """
  segments = []
  with open(file_name, encoding="utf-8") as f:
    for line in f:
      segments.append(segment({'text': line.strip()}))
  return segments
