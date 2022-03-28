#!/usr/bin/env python
"""
Test wer calculation
"""

import json

from utils import get_sample_dir, get_test_dir

from asrtoolkit.data_structures import Transcript

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def test_json_initialization():
    "execute single test"

    input_dict = json.load(open(f"{sample_dir}/BillGatesTEDTalk.json"))
    text_object = Transcript(input_dict, file_format="greenkey")

    ref = (
        open(f"{sample_dir}/BillGatesTEDTalk_transcribed.stm", "r", encoding="utf8")
        .read()
        .strip()
    )
    text_object.write(f"{test_dir}/file_conversion_test.stm")
    new = (
        open(f"{test_dir}/file_conversion_test.stm", "r", encoding="utf8")
        .read()
        .strip()
    )
    assert ref == new


def test_txt_initialization():
    "execute single test"

    input_dict = json.load(open(f"{sample_dir}/BillGatesTEDTalk.json"))
    text = Transcript(input_dict, file_format="greenkey")
    text.file_extension = "txt"

    text_object = Transcript(text.__str__())

    ref = (
        open(f"{sample_dir}/BillGatesTEDTalk_transcribed.txt", "r", encoding="utf8")
        .read()
        .strip()
    )
    text_object.write(f"{test_dir}/file_conversion_test.txt")
    new = (
        open(f"{test_dir}/file_conversion_test.txt", "r", encoding="utf8")
        .read()
        .strip()
    )
    assert ref == new


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
