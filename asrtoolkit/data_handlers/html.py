#!/usr/bin/env python
"""
Module for handling HTML file io

Note that the structure may change without notice and break backwards compatibility
This expects a segment from class derived in convert_text
"""

from bs4 import BeautifulSoup
from asrtoolkit.data_structures.segment import segment

# do not delete - needed in time_aligned_text
from asrtoolkit.data_handlers.data_handlers_common import separator


def th(text, width):
  " make a table delimiter with input width "
  return "<th align=\"left\" width=\"{:}%\">{:}</th>".format(width, text)


def td(text):
  " make a table delimiter element "
  return "<td align=\"left\">{:}</td>".format(text)


def header():
  " Returns html header "

  widths = [10, 8, 82]

  return "<table>\n<tr>" + "".join(
    th(t, w) for t, w in zip(["[Start time - End time]", "Speaker", "Transcript"], widths)
  ) + "</tr>\n"


def footer():
  " Returns html footer "
  return "</table>\n"


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    filename, channel, speaker, start and stop times, label, and text
  """

  return "<tr>" + "".join(
    td(t) for t in
    ["[{:} - {:}]".format(seg.start, seg.stop), seg.speaker, seg.formatted_text if seg.formatted_text else seg.text]
  ) + "</tr>\n"


def parse_line(line):
  " parse a single line of an html file"
  cols = line.findAll('td')
  seg = None
  if cols:
    start_stop, speaker, text = [[val for val in col.children][0] for col in cols]
    start, stop = start_stop[1:-1].split(" - ")
    seg = segment({'speaker': speaker, 'start': start, 'stop': stop, 'text': text})
    seg = seg if seg.validate() else None
  return seg


def read_file(file_name):
  """
    Reads an HTML file, skipping any gap lines
  """
  soup = BeautifulSoup(open(file_name).read(), "html.parser")
  table = soup.find("table", {})

  segments = [_ for _ in map(parse_line, table.findAll('tr')) if _]

  return segments
