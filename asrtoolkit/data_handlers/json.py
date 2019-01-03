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
    filename, channel, speaker, start and stop times, label, and text

  :param: seg: segment object
  :return: dict: key/val pairs contain 'segment'-level information
    values of output segment-dict are values of corresponding input segment attributes

      output_dict['startTimeSec'] = segment.start          (converse of parse_segment)

    the segment dict structure generated is the output of all microservices and input to most
      each segment-dict contains a fragment of text (+ additional information)
  """
  output_dict = {}
  output_dict['speakerInfo'] = seg.speaker
  output_dict['startTimeSec'] = seg.start
  output_dict['endTimeSec'] = seg.stop
  output_dict['genderInfo'] = {'gender': seg.label.split(",")[-1].replace(">", "")}
  output_dict['punctuated_transcript'] = seg.formatted_text
  output_dict['transcript'] = seg.text
  output_dict['confidence'] = seg.confidence

  return json.dumps(output_dict, ensure_ascii=True)


def parse_segment(input_seg):
  """
    Creates a segment object from an input GreenKey segment
  :param: input_seg: dict  (segment-level dict: input_data['segments'][i]['segment'])
      -> dict with keys 'channel', 'startTimeSec' etc mapping to segment object attributes

  :return: segment object; attribute values are set to those of corresponding segment-dict keys

      segment.start = segment_dict['startTimeSec']         (reverse mapping from format_segment)
  """
  extracted_dict = {}

  def assign_if_present(value, dict_key=None, interior_key=None, proc_val=lambda val: val):
    """
    :param value: type?
    :param dict_key:
    :param interior_key:
    :param proc_val:
    :return: type?

      Assigns value to extracted_dict object if present in input_seg
    """
    dict_key = value if dict_key is None else dict_key

    if value in input_seg and interior_key and interior_key in input_seg[value]:
      extracted_dict[dict_key] = proc_val(input_seg[value][interior_key])
    elif value in input_seg and not interior_key:
      extracted_dict[dict_key] = proc_val(input_seg[value])

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
    assign_if_present('confidence', 'confidence')

    seg = segment(extracted_dict)

  except Exception as exc:
    print(exc)      #TODO log instead

  return seg if seg and seg.validate() else None


def read_in_memory(input_data):
  """
    Reads input json objects

  :param: input_data: dict with key 'segments'
    input_data['segments']: List[Dict]; each dict has key 'segment' with a dict as the value (segment_dict)
    - segment_dicts contain key/val pairs that map to `segment` object attributes
    - labels of mapped key-attribute pairs may differ: segment['startTimeSec'] -> segment.start

  :return: list of segment objects
    applies parse_segment function to each dict in input_data['segments']
     - func creates a `segment` object for each segment_dict, mapping corresponding attributes

  input_data['segments'][i]['segment'] --> mapped to ith segment object (with 'start', 'stop' etc'
  """
  segments = [_ for _ in map(parse_segment, input_data['segments']) if _ is not None]
  return segments


def read_file(file_name):
  """
    Reads a JSON file, skipping any bad segments
  """
  with open(file_name, encoding="utf-8") as f:
    input_json = json.load(f)
    segments = read_in_memory(input_json)
  return segments
