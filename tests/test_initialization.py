#!/usr/bin/env python
"""
Test wer calculation
"""

import hashlib
import json

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text

from utils import get_sample_dir, get_test_dir

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def test_json_initialization():
    " execute single test "

    input_dict = json.load(open(f"{sample_dir}/BillGatesTEDTalk.json"))
    text_object = time_aligned_text(input_dict)

    reference_sha = hashlib.sha1(
        open(f"{sample_dir}/BillGatesTEDTalk_transcribed.stm", "r", encoding="utf8")
        .read()
        .encode()
    ).hexdigest()
    text_object.write(f"{test_dir}/file_conversion_test.stm")
    new_sha = hashlib.sha1(
        open(f"{test_dir}/file_conversion_test.stm", "r", encoding="utf8")
        .read()
        .encode()
    ).hexdigest()
    assert reference_sha == new_sha


def test_txt_initialization():
    " execute single test "

    input_dict = json.load(open(f"{sample_dir}/BillGatesTEDTalk.json"))
    text = time_aligned_text(input_dict)
    text.file_extension = "txt"

    text_object = time_aligned_text(text.__str__())

    reference_sha = hashlib.sha1(
        open(f"{sample_dir}/BillGatesTEDTalk_transcribed.txt", "r", encoding="utf8")
        .read()
        .encode()
    ).hexdigest()
    text_object.write(f"{test_dir}/file_conversion_test.txt")
    new_sha = hashlib.sha1(
        open(f"{test_dir}/file_conversion_test.txt", "r", encoding="utf8")
        .read()
        .encode()
    ).hexdigest()
    assert reference_sha == new_sha


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
