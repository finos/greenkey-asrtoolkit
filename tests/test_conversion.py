#!/usr/bin/env python
"""
Test file conversion using samples
"""

import hashlib


def test_conversion():
  " execute file conversion tests "

  from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.txt")
  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.txt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.txt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha

  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.html", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  input_file.write("file_conversion_test.html")
  new_sha = hashlib.sha1(open("file_conversion_test.html", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha

  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.vtt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  input_file.write("file_conversion_test.vtt")
  new_sha = hashlib.sha1(open("file_conversion_test.vtt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha

  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.srt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  input_file.write("file_conversion_test.srt")
  new_sha = hashlib.sha1(open("file_conversion_test.srt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha

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
