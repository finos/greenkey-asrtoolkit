#!/usr/bin/env python
"""
Test wer calculation
"""

from asrtoolkit.wer import wer
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text


def test_conversion():
  " execute single test "

  reference_file = time_aligned_text("samples/BillGatesTEDTalk.stm")
  transcript_file = time_aligned_text("samples/BillGatesTEDTalk_intentionally_poor_transcription.txt")

  # test fixed precision output of wer calculation
  assert "{:5.3f}".format(wer(reference_file.text(), transcript_file.text(), True)) == "3.332"


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
