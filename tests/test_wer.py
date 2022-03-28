#!/usr/bin/env python
"""
Test wer calculation
"""

from utils import get_sample_dir

from asrtoolkit.data_structures import Transcript
from asrtoolkit.metrics import cer, wer

sample_dir = get_sample_dir(__file__)


def test_conversion_wer():
    "execute single test"

    reference_file = Transcript(f"{sample_dir}/BillGatesTEDTalk.stm")
    transcript_file = Transcript(
        f"{sample_dir}/BillGatesTEDTalk_intentionally_poor_transcription.txt"
    )

    # test fixed precision output of wer calculation
    assert (
        "{:5.3f}".format(wer(reference_file.text(), transcript_file.text(), True))
        == "3.332"
    )


def test_non_ascii():
    """
    Test WER for non-ascii characters
    """

    ref = """﻿﻿정답입니다
정답 이에요
삐약"""
    hyp = """﻿﻿정답 입 니다
정답 이에요
하이륭"""

    assert wer(ref, hyp) == 100.0

    assert cer(ref, hyp) == 100.0 / 3.0


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
