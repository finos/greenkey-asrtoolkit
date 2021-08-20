#!/usr/bin/env python
"""
Test file conversion using samples
"""
import os
import hashlib

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from utils import get_sample_dir, get_test_dir

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def test_stm_to_txt_conversion():
    " execute stm to txt test "

    transcript = time_aligned_text(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_txt_test.txt")


def test_stm_to_html_conversion():
    " execute stm to html test "

    transcript = time_aligned_text(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_html_test.html")


def test_stm_to_vtt_conversion():
    " execute stm to vtt test "

    transcript = time_aligned_text(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_vtt_test.vtt")


def test_stm_to_srt_conversion():
    " execute stm to srt test "

    transcript = time_aligned_text(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_srt_test.srt")


def test_json_to_stm_conversion():
    " execute json to stm tests "

    transcript = time_aligned_text(f"{sample_dir}/BillGatesTEDTalk.json")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_stm_test_1.stm")

    transcript = time_aligned_text(f"{sample_dir}/simple_test.json")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_stm_test_2.stm")


def test_json_to_txt_conversion():
    " execute json to txt test "

    transcript = time_aligned_text(f"{sample_dir}/simple_test.json")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_txt_test.txt")


def test_json_to_rttm_conversion():
    """
    execute json to rttm test
    """
    transcript = time_aligned_text(f"{sample_dir}/simple_test.json")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_rttm_test.rttm")


def test_json_to_rttm_conversion_without_speaker():
    """
    execute json to rttm test
    """
    transcript = time_aligned_text(f"{test_dir}/no_speaker.json")

    convert_and_test_it_loads(transcript, f"{test_dir}/no_speaker.rttm")


def convert_and_test_it_loads(transcript_obj, output_filename):
    """
    Tests that conversion works
    Tests that the file can reload
    Removes transitory file
    """
    transcript_obj.write(output_filename)
    time_aligned_text(output_filename)

    os.remove(output_filename)


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
