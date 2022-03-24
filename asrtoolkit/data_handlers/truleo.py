#!/usr/bin/env python
"""
Module for reading/writing gk JSON files
"""

import json
import logging

from asrtoolkit.data_structures.segment import segment
from asrtoolkit.file_utils.name_cleaners import sanitize

LOGGER = logging.getLogger(__name__)
separator = ",\n"


def header():
    "Returns empty header"
    return '{\n"segments":['


def footer():
    "Returns empty footer"
    return "]}\n"


def format_segment(seg):
    """
    Formats a segment assuming it's an instance of class segment with elements
    filename, channel, speaker, start and stop times, label, and text

    :param: seg: segment object
    :return: dict: key/val pairs contain 'segment'-level information
    """
    output_dict = {}
    output_dict["speaker"] = {"label": seg.speaker, "confidence": 0.0}
    output_dict["start"] = float(seg.start) * 1e3
    output_dict["stop"] = float(seg.stop) * 1e3
    output_dict["tokens"] = [
        {
            "token": word,
            "asr_confidence": 0.0,
            "label_confidence": 0.0,
            "start": 0,
            "stop": 0.0,
            "label": "O",
        }
        for word in seg.text.split()
    ]
    output_dict["asr_confidence"] = seg.confidence

    return json.dumps(output_dict, ensure_ascii=True)


def parse_segment(input_seg):
    """
    Creates an asrtoolkit segment object from an input gk segment
    :param: input_seg: dict (segment-level dict: input_data['segments'][i]
      -> dict with keys 'channel', 'startTimeSec' etc mapping to attributes
    :return: asrtoolkit segment object
    """
    extracted_dict = {}

    def assign_if_present(
        value, dict_key=None, interior_key=None, proc_val=lambda val: val
    ):
        """
        This transforms gk segment data into a dictionary for input
        into the asrtoolkit segment object

        Assigns value to extracted_dict object if present in input_seg

        :param value:         key from the inside of gk segment
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
        assign_if_present("channel")
        assign_if_present("start", "start", proc_val=lambda val: float(val) / 1e3)
        assign_if_present("stop", "stop", proc_val=lambda val: float(val) / 1e3)
        assign_if_present(
            "tokens",
            "text",
            proc_val=lambda token_list: " ".join(
                token["token"] for token in token_list
            ),
        )
        assign_if_present("speaker", "speaker", "label", proc_val=sanitize)
        assign_if_present("asr_confidence", "confidence")

        seg = segment(extracted_dict)

    except Exception as exc:
        LOGGER.exception(exc)

    return seg if seg and seg.validate() else None


def read_in_memory(input_data):
    """
    Reads input json objects

    :param: input_data: dict with key 'segments'
      input_data['segments']: List[Dict];
      - segment_dicts contain key/val pairs that map to `segment` attributes
        NB that labels of mapped key-attribute pairs may differ
          for example, segment['startTimeSec'] -> segment.start

    :return: list of segment objects
      applies `parse_segment` function to each dict in input_data['segments']

    """
    segments = [_ for _ in map(parse_segment, input_data["segments"]) if _ is not None]
    return segments


def read_file(file_name):
    """
    Reads a JSON file, skipping any bad segments
    """
    with open(file_name, encoding="utf-8") as f:
        input_json = json.load(f)
        segments = read_in_memory(input_json)
    return segments