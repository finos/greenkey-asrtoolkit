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

  seg = None
  try:
    extracted_dict = {}
    if 'channel' in input_seg:
      extracted_dict['channel'] = input_seg['channel']

    if 'speakerInfo' in input_seg:
      extracted_dict['speaker'] = input_seg['speakerInfo']

    if 'startTimeSec' in input_seg:
      extracted_dict['start'] = input_seg['startTimeSec']

    if 'endTimeSec' in input_seg:
      extracted_dict['stop'] = input_seg['endTimeSec']

    if 'genderInfo' in input_seg and 'gender' in input_seg['genderInfo']:
      extracted_dict['label'] = "<o,f0,{:}>".format(input_seg['genderInfo']['gender'])

    if 'transcript' in input_seg:
      extracted_dict['text'] = input_seg['transcript']

    extracted_dict['formatted_text'] = input_seg['punctuated_transcript'] if 'punctuated_transcript' in input_seg else (
      input_seg['formatted_transcript'] if 'formatted_transcript' in input_seg else ""
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
  if 'segments' in input_data:
    for input_seg in input_data['segments']:
      seg = parse_segment(input_seg)
      if seg is not None:
        segments.append(seg)
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
