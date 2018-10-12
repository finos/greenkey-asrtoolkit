#!/usr/bin/env python
"""
Module for reading/writing WEBVTT files

This expects a segment from class derived in convert_text
"""

from webvtt import WebVTT
from asrtoolkit.data_handlers.webvtt_common import read_caption
from asrtoolkit.data_structures.segment import seconds_to_timestamp

# do not delete - needed for time_aligned_text
from asrtoolkit.data_handlers.data_handlers_common import separator, footer


def header():
  " Returns header - see https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API for detailed use "
  return "WEBVTT - This file produced by GreenKey's ASRToolkit.\n\n"


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    audiofile, channel, speaker, start and stop times, label, and text
  """

  ret_str = "{:} --> {:}".format(seconds_to_timestamp(seg.start), seconds_to_timestamp(seg.stop))
  ret_str += " <v Channel {:}>".format(seg.channel)
  ret_str += " <v Speaker {:}>".format(seg.speaker)
  ret_str += "\n{:}\n".format(seg.formatted_text if seg.formatted_text else seg.text)

  return ret_str


def read_file(file_name):
  """
    Reads a VTT file, skipping any bad lines
  """

  data = WebVTT.read(file_name)
  captions = data.captions

  segments = []
  for caption in captions:
    seg = read_caption(caption)
    if seg is not None:
      segments.append(seg)

  return segments
