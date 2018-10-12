#!/usr/bin/env python
"""
Test file conversion using samples
"""

import hashlib

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text


def test_stm_to_txt_conversion():
  " execute stm to txt test "

  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.txt")
  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.txt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.txt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


def test_stm_to_html_conversion():
  " execute stm to html test "

  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.html")
  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.html", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.html", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


def test_stm_to_vtt_conversion():
  " execute stm to vtt test "

  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.vtt")

  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.vtt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.vtt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


def test_stm_to_srt_conversion():
  " execute stm to srt test "

  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.srt")

  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.srt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.srt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


def test_json_to_stm_conversion():
  " execute json to stm test "

  input_file = time_aligned_text("../samples/BillGatesTEDTalk.json")
  reference_sha = hashlib.sha1(
    open("../samples/BillGatesTEDTalk_transcribed.stm", 'r', encoding='utf8').read().encode()
  ).hexdigest()
  input_file.write("file_conversion_test.stm")
  new_sha = hashlib.sha1(open("file_conversion_test.stm", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
