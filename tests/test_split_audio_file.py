#!/usr/bin/env python
"""
Test audio file splitter
"""
import os
from asrtoolkit.split_audio_file import split_audio_file


def test_split_audio_file():
    " test audio file splitter "
    split_audio_file("tests/small-test-file.mp3", "tests/small-test-file.stm", "tests/split")
    assert set(os.listdir("tests/split"))=={'small_test_file_seg_00001.stm', 'small_test_file_seg_00000.mp3', 'small_test_file_seg_00001.mp3', 'small_test_file_seg_00000.stm'}



if __name__ == '__main__':
    import sys
    import pytest
    pytest.main(sys.argv)
