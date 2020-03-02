#!/usr/bin/env python3
"""
Test to ensure that alignment can work
"""
import hashlib

from asrtoolkit.align_json import align_json


def test_simple_alignment():
    align_json("samples/BillGatesTEDTalk.txt", "samples/BillGatesTEDTalk.json",
               "tests/BillGatesTEDTalk_aligned.stm")
    new_sha = hashlib.sha1(
        open("tests/BillGatesTEDTalk_aligned.stm", "r",
             encoding="utf8").read().encode()).hexdigest()
    reference_sha = "0d4a20cf54fdc2834c69d9697c5820556139379e"
    assert reference_sha == new_sha


if __name__ == "__main__":
    import sys
    import pytest

    pytest.main(sys.argv)
