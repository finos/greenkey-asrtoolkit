#!/usr/bin/env python
"""
Module for reading STM files

Expected file format is derived from http://www1.icsi.berkeley.edu/Speech/docs/sctk-1.2/infmts.htm#stm_fmt_name_0

This expects a segment from class derived in convert_text
"""

from asrtoolkit.data_structures.segment import segment

separator = "\n"


def header():
  " Returns empty header "
  return ""


def footer():
  " Returns empty footer "
  return ""


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    audiofile, channel, speaker, start and stop times, label, and text
  """
  return " ".join(str(seg.__dict__[_]) for _ in ('audiofile', 'channel', 'speaker', 'start', 'stop', 'label', 'text'))


def parse_line(line):
  " parse a single line of an stm file"

  data = line.strip().split()

  seg = None
  if len(data) > 6:
    audiofile, channel, speaker, start, stop, label = data[:6]
    text = " ".join(data[6:])
    seg = segment(
      {
        'audiofile': audiofile,
        'channel': channel,
        'speaker': speaker,
        'start': start,
        'stop': stop,
        'label': label,
        'text': text
      }
    )
  return seg if seg and seg.validate() else None


def read_file(file_name):
  """
    Reads an STM file, skipping any gap lines
  """
  segments = []
  with open(file_name, encoding="utf-8") as f:
    for line in f:
      seg = parse_line(line)
      if seg is not None:
        segments.append(seg)

  return segments
