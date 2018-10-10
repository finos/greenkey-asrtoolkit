#!/usr/bin/env python
"""
Module for reading/writing SRT files

This expects a segment from class derived in convert_text
"""

import re
from webvtt import WebVTT
from asrtoolkit.data_structures.segment import segment, seconds_to_timestamp

non_transcript_marks = re.compile(r"\[[A-Za-z0-9]{1,}\]")

separator = "\n"


def header():
  " Returns header "
  return ""


def footer():
  " Returns footer "
  return ""


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    audiofile, channel, speaker, start and stop times, label, and text
  """

  ret_str = "1\n{:} --> {:}\n".format(seconds_to_timestamp(seg.start), seconds_to_timestamp(seg.stop)).replace(".", ",")
  ret_str += "{:}\n\n".format(seg.formatted_text if seg.formatted_text else seg.text)

  return ret_str


def read_caption(caption):
  """
    Parses caption object to return a segment object
  """
  seg = None

  try:
    start = caption.start_in_seconds
    stop = caption.end_in_seconds

    text = re.sub(non_transcript_marks, lambda v: "", caption.text.strip()).strip()

    seg = segment({'start': start, 'stop': stop, 'text': text})
  except Exception as exc:
    seg = None
    print(exc)

  return seg if seg and seg.validate() else None


def read_file(file_name):
  """
    Reads an SRT file, skipping any bad lines
  """

  data = WebVTT.from_srt(file_name)
  captions = data.captions

  segments = []
  for caption in captions:
    seg = read_caption(caption)
    if seg is not None:
      segments.append(seg)

  return segments
