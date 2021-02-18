#!/usr/bin/env python
"""
Test wer calculation
"""

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.wer import cer, wer


def test_conversion_wer():
    " execute single test "

    reference_file = time_aligned_text("samples/BillGatesTEDTalk.stm")
    transcript_file = time_aligned_text(
        "samples/BillGatesTEDTalk_intentionally_poor_transcription.txt"
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
