#!/usr/bin/env python
"""
Module for reading STM files

Expected file format is derived from http://www1.icsi.berkeley.edu/Speech/docs/sctk-1.2/infmts.htm#stm_fmt_name_0

This expects a segment from class derived in convert_text
"""

from asrtoolkit.data_structures.segment import segment
from asrtoolkit.clean_formatting import clean_up

# leave in place for other imports
from asrtoolkit.data_handlers.data_handlers_common import separator, header, footer


def format_segment(seg):
  """
  :param seg: segment object
  :return str: text for a particular STM line (see segment __str__ method)
    Formats a segment assuming it's an instance of class segment with elements
    filename, channel, speaker, start and stop times, label, and text
  """
  return " ".join(
    [str(seg.__dict__[_]) for _ in ('filename', 'channel', 'speaker', 'start', 'stop', 'label')] +
    [clean_up(seg.__dict__['text'])]  # clean_up used to unformat stm file text
  )


def parse_line(line):
  """
  :param line: str; a single line of an stm file
  :return: segment object if STM file line contains accurately formatted data; else None
  """
  data = line.strip().split()

  seg = None
  if len(data) > 6:
    filename, channel, speaker, start, stop, label = data[:6]
    text = " ".join(data[6:])
    seg = segment(
      {
        'filename': filename,
        'channel': channel,
        'speaker': speaker,
        'start': start,
        'stop': stop,
        'label': label,
        'text': text,
      }
    )
  return seg if seg and seg.validate() else None


def read_file(file_name):
  """
    Reads an STM file, skipping any gap lines
    :return: list of segment objects
  """
  segments = []
  with open(file_name, encoding="utf-8") as f:
    for line in f:
      seg = parse_line(line)
      if seg is not None:
        segments.append(seg)
  return segments
