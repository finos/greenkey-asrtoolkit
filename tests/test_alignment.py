#!/usr/bin/env python3
"""
Test to ensure that alignment can work
"""

from asrtoolkit import align_json, time_aligned_text
from utils import get_sample_dir, get_test_dir

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def test_simple_alignment():
    align_json(
        f"{sample_dir}/BillGatesTEDTalk.txt",
        f"{sample_dir}/BillGatesTEDTalk.json",
        f"{test_dir}/BillGatesTEDTalk_aligned.stm",
    )

    aligned_transcript = time_aligned_text(f"{test_dir}/BillGatesTEDTalk_aligned.stm")
    assert len(aligned_transcript.segments) == 104


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
