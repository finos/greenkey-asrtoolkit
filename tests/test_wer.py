#!/usr/bin/env python
"""
Test wer calculation
"""

from asrtoolkit.wer import wer, remove_nonsilence_noises
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.clean_formatting import clean_up


def test_conversion():
  " execute single test "

  reference_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  transcript_file = time_aligned_text("../samples/BillGatesTEDTalk_intentionally_poor_transcription.txt")

  # note that we need to set the extensions to txt in order to get only txt back from the __str__ function
  reference_file.file_extension = 'txt'
  transcript_file.file_extension = 'txt'

  # apply clean up functions and split to a list of lines
  ref = clean_up(reference_file.__str__()).splitlines()
  hyp = clean_up(transcript_file.__str__()).splitlines()

  # remove nsns
  ref = [clean_up(remove_nonsilence_noises(line).strip()) for line in ref]
  hyp = [clean_up(remove_nonsilence_noises(line).strip()) for line in hyp]

  # test fixed precision output of wer calculation
  assert "{:5.3f}".format(wer(ref, hyp)) == "3.332"


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
