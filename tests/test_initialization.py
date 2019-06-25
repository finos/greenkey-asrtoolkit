#!/usr/bin/env python
"""
Test wer calculation
"""

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
import json
import hashlib


def test_json_initialization():
  " execute single test "

  input_dict = json.load(open("samples/BillGatesTEDTalk.json"))
  text_object = time_aligned_text(input_dict)

  reference_sha = hashlib.sha1(open("samples/BillGatesTEDTalk_transcribed.stm", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  text_object.write("tests/file_conversion_test.stm")
  new_sha = hashlib.sha1(open("tests/file_conversion_test.stm", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


def test_txt_initialization():
  " execute single test "

  input_dict = json.load(open("samples/BillGatesTEDTalk.json"))
  text = time_aligned_text(input_dict)
  text.file_extension = 'txt'

  text_object = time_aligned_text(text.__str__())

  reference_sha = hashlib.sha1(open("samples/BillGatesTEDTalk_transcribed.txt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  text_object.write("tests/file_conversion_test.txt")
  new_sha = hashlib.sha1(open("tests/file_conversion_test.txt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
