#!/usr/bin/env python
"""
Test file conversion using samples
"""

import hashlib


def test_conversion():
  " execute single test "

  from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.txt")
  reference_sha = hashlib.sha1(open("../samples/BillGatesTEDTalk.txt", 'r',
                                    encoding='utf8').read().encode()).hexdigest()
  new_sha = hashlib.sha1(open("file_conversion_test.txt", 'r', encoding='utf8').read().encode()).hexdigest()
  assert reference_sha == new_sha


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
