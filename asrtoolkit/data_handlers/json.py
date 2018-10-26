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


def assign_if_present(seg, output_dict, value, dict_key=None, interior_key=None, proc_val=lambda val: val):
  """
  Assigns value to object if present
  """

  dict_key = value if dict_key is None else dict_key

  if value in seg:
    output_dict[dict_key] = proc_val(seg[value] if interior_key is None else seg[value][interior_key])
  return output_dict


def parse_segment(input_seg):
  """
    Creates a segment object from an input GreenKey segment
  """

  seg = None
  try:
    extracted_dict = {}
    extracted_dict = assign_if_present(seg, extracted_dict, 'channel')
    extracted_dict = assign_if_present(seg, extracted_dict, 'startTimeSec', 'start')
    extracted_dict = assign_if_present(seg, extracted_dict, 'stopTimeSec', 'stop')
    extracted_dict = assign_if_present(seg, extracted_dict, 'endTimeSec', 'stop')
    extracted_dict = assign_if_present(seg, extracted_dict, 'transcript', 'text')
    extracted_dict = assign_if_present(seg, extracted_dict, 'formatted_transcript', 'formatted_text')
    extracted_dict = assign_if_present(seg, extracted_dict, 'punctuated_transcript', 'formatted_text')
    extracted_dict = assign_if_present(seg, extracted_dict, 'speakerInfo', 'speaker', 'ID')
    extracted_dict = assign_if_present(
      seg, extracted_dict, 'genderInfo', 'label', 'gender', lambda gender: "<o,f0,{:}>".format(gender)
    )

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
