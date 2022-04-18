#!/usr/bin/env python
"""
Module for reading/writing gong.io gecko JSON files
"""

import json
import logging

from asrtoolkit.data_structures import Segment
from asrtoolkit.file_utils.name_cleaners import sanitize

LOGGER = logging.getLogger(__name__)
separator = ",\n"


def header():
    "Returns empty header"
    return '{\n"schemaVersion": "2.0","monologues":['


def footer():
    "Returns empty footer"
    return "]}\n"


def format_segment(seg):
    """
    Formats a Segment assuming it's an instance of class Segment with elements
    filename, channel, speaker, start and stop times, label, and text

    :param: seg: Segment object
    :return: dict: key/val pairs contain 'segment'-level information
    """
    output_dict = {}
    output_dict["speaker"] = {"id": seg.speaker, "name": ""}
    output_dict["start"] = float(seg.start)
    output_dict["stop"] = float(seg.stop)

    # don't approximate word start and stop times, just shove them all in one term for now
    output_dict["terms"] = [
        {
            "start": float(seg.start),
            "end": float(seg.stop),
            "text": seg.text,
            "type": "WORD",
        }
    ]
    return json.dumps(output_dict, ensure_ascii=True)


def parse_segment(input_seg):
    """
    Creates an asrtoolkit Segment object from an input gecko segment
    :param: input_seg: dict (segment-level dict: input_data['segments'][i]
      -> dict with keys 'channel', 'startTimeSec' etc mapping to attributes
    :return: asrtoolkit Segment object
    """
    extracted_dict = {}

    def assign_if_present(
        value, dict_key=None, interior_key=None, proc_val=lambda val: val
    ):
        """
        This transforms gecko segment data into a dictionary for input
        into the asrtoolkit Segment object

        Assigns value to extracted_dict object if present in input_seg

        :param value:         key from the inside of the Segment
        :param dict_key:      key to which value should be assigned
        :param interior_key:  sometimes values are nested under this
        :param proc_val:      function formatting the value

        """
        dict_key = value if dict_key is None else dict_key
        ret_val = None
        if value in input_seg and interior_key and interior_key in input_seg[value]:
            ret_val = proc_val(input_seg[value][interior_key])
        elif value in input_seg and not interior_key:
            ret_val = proc_val(input_seg[value])
        if ret_val not in {"", None}:
            extracted_dict[dict_key] = ret_val

    seg = None
    try:
        assign_if_present("start", "start")
        assign_if_present("end", "stop")
        assign_if_present(
            "terms",
            "text",
            proc_val=lambda term_list: " ".join(term["text"] for term in term_list),
        )
        assign_if_present(
            "speaker", "speaker", "id", proc_val=sanitize,
        )

        seg = Segment(extracted_dict)

    except Exception as exc:
        LOGGER.exception(exc)

    return seg if seg and seg.validate() else None


def read_in_memory(input_data):
    """
    Reads input json objects

    :param: input_data: dict with key 'segments'
      input_data['segments']: List[Dict];
      - Segment_dicts contain key/val pairs that map to `segment` attributes
        NB that labels of mapped key-attribute pairs may differ
          for example, Segment['startTimeSec'] -> Segment.start

    :return: list of Segment objects
      applies `parse_segment` function to each dict in input_data['segments']

    """
    segments = [
        _ for _ in map(parse_segment, input_data["monologues"]) if _ is not None
    ]
    return segments


def read_file(file_name):
    """
    Reads a JSON file, skipping any bad Segments
    """
    with open(file_name, encoding="utf-8") as f:
        input_json = json.load(f)
        segments = read_in_memory(input_json)
    return segments
