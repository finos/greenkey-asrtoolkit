#!/usr/bin/env python
"""
Module for reading/writing SRT files

This expects a segment from class derived in convert_text
"""

from webvtt import WebVTT
from asrtoolkit.data_handlers.webvtt_common import read_caption
from asrtoolkit.data_structures.segment import seconds_to_timestamp

# do not delete - needed in time_aligned_text
from asrtoolkit.data_handlers.data_handlers_common import separator, header, footer


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    filename, channel, speaker, start and stop times, label, and text
  """

  ret_str = "1\n{:} --> {:}\n".format(seconds_to_timestamp(seg.start), seconds_to_timestamp(seg.stop)).replace(".", ",")
  ret_str += "{:}\n\n".format(seg.formatted_text if seg.formatted_text else seg.text)

  return ret_str


def read_file(file_name):
  """ Reads an SRT file """

  data = WebVTT.from_srt(file_name)
  captions = data.captions

  segments = []
  for caption in captions:
    seg = read_caption(caption)
    if seg is not None:
      segments.append(seg)

  return segments
