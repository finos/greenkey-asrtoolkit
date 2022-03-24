#!/usr/bin/env python
"""
Test audio file splitter
"""
import os

from utils import get_test_dir

from asrtoolkit.split_audio_file import split_audio_file

test_dir = get_test_dir(__file__)


def test_split_audio_file():
    """
    Test audio file splitter
    """
    split_audio_file(
        f"{test_dir}/small-test-file.mp3",
        f"{test_dir}/small-test-file.stm",
        f"{test_dir}/split",
    )
    assert set(os.listdir(f"{test_dir}/split")) == {
        "small_test_file_seg_00001.stm",
        "small_test_file_seg_00000.mp3",
        "small_test_file_seg_00001.mp3",
        "small_test_file_seg_00000.stm",
    }


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
