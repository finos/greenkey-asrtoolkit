#!/usr/bin/env python
"""
Module for reading/writing JSON files

This expects a segment from class derived in convert_text
"""

from asrtoolkit.data_structures.segment import segment
import json

separator = ",\n"


def header():
  " Returns empty header "
  return "{\n\"segments\":["


def footer():
  " Returns empty footer "
  return "]}\n"


def format_segment(seg):
  """
    Formats a segment assuming it's an instance of class segment with elements
    audiofile, channel, speaker, start and stop times, label, and text
  """
  output_dict = {}
  output_dict['speakerInfo'] = seg.speaker
  output_dict['startTimeSec'] = seg.start
  output_dict['endTimeSec'] = seg.stop
  output_dict['genderInfo'] = {'gender': seg.label.split(",")[-1].replace(">", "")}
  output_dict['punctuated_transcript'] = seg.formatted_text
  output_dict['transcript'] = seg.text

  return json.dumps(output_dict, ensure_ascii=True)


def parse_segment(input_seg):
  """
    Creates a segment object from an input GreenKey segment
  """

  extracted_dict = {}

  def assign_if_present(value, dict_key=None, interior_key=None, proc_val=lambda val: val):
    """
      Assigns value to extracted_dict object if present in input_seg
    """

    dict_key = value if dict_key is None else dict_key

    if value in input_seg:
      extracted_dict[dict_key] = proc_val(input_seg[value] if interior_key is None else input_seg[value][interior_key])

  seg = None
  try:
    assign_if_present('channel')
    assign_if_present('startTimeSec', 'start')
    assign_if_present('stopTimeSec', 'stop')
    assign_if_present('endTimeSec', 'stop')
    assign_if_present('transcript', 'text')
    assign_if_present('corrected_transcript', 'text')
    assign_if_present('formatted_transcript', 'formatted_text')
    assign_if_present('punctuated_transcript', 'formatted_text')
    assign_if_present('speakerInfo', 'speaker', 'ID')
    assign_if_present('genderInfo', 'label', 'gender', lambda gender: "<o,f0,{:}>".format(gender))

    seg = segment(extracted_dict)

  except Exception as exc:
    print(exc)

  return seg if seg and seg.validate() else None


def read_in_memory(input_data):
  """
    Reads input json objects
  """
  segments = []
  segments = [_ for _ in map(parse_segment, input_data['segments']) if _ is not None]
  return segments


def read_file(file_name):
  """
    Reads a JSON file, skipping any bad segments
  """
  segments = []
  with open(file_name, encoding="utf-8") as f:
    input_json = json.load(f)
    segments = read_in_memory(input_json)

  return segments
