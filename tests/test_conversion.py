#!/usr/bin/env python
"""
Test file conversion using samples
"""
import os

from utils import get_sample_dir, get_test_dir

from asrtoolkit.data_structures import Transcript

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def test_stm_to_txt_conversion():
    "execute stm to txt test"

    transcript = Transcript(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_txt_test.txt")


def test_stm_to_html_conversion():
    "execute stm to html test"

    transcript = Transcript(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_html_test.html")


def test_stm_to_vtt_conversion():
    "execute stm to vtt test"

    transcript = Transcript(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_vtt_test.vtt")


def test_stm_to_srt_conversion():
    "execute stm to srt test"

    transcript = Transcript(f"{sample_dir}/BillGatesTEDTalk.stm")
    convert_and_test_it_loads(transcript, f"{test_dir}/stm_to_srt_test.srt")


def test_json_to_stm_conversion():
    "execute json to stm tests"

    transcript = Transcript(
        f"{sample_dir}/BillGatesTEDTalk.json", file_format="greenkey"
    )
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_stm_test_1.stm")

    transcript = Transcript(f"{sample_dir}/simple_test.json", file_format="greenkey")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_stm_test_2.stm")


def test_json_to_txt_conversion():
    "execute json to txt test"

    transcript = Transcript(f"{sample_dir}/simple_test.json", file_format="greenkey")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_txt_test.txt")


def test_json_to_rttm_conversion():
    """
    execute json to rttm test
    """
    transcript = Transcript(f"{sample_dir}/simple_test.json", file_format="greenkey")
    convert_and_test_it_loads(transcript, f"{test_dir}/json_to_rttm_test.rttm")


def test_json_to_rttm_conversion_without_speaker():
    """
    execute json to rttm test
    """
    transcript = Transcript(f"{test_dir}/no_speaker.json", file_format="greenkey")

    convert_and_test_it_loads(transcript, f"{test_dir}/no_speaker.rttm")


def convert_and_test_it_loads(transcript_obj, output_filename):
    """
    Tests that conversion works
    Tests that the file can reload
    Removes transitory file
    """
    transcript_obj.write(output_filename)
    Transcript(output_filename)

    os.remove(output_filename)


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
