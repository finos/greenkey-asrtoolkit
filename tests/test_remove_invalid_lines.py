#!/usr/bin/env python
"""
Test invalid line removal
"""

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.convert_transcript import convert


EXPECTED_UNFORMATTED_TRANSCRIPTS = (
    'testing testing one two three or maybe ten four',
    'testing testing one two three',
    'testing testing one two three'
)

EXPECTED_FORMATTED_TRANSCRIPTS = (
    'testing testing one two three or maybe 10 4',
    'testing testing one two three',
    'testing testing, one two three!'
)

def validate_sample(ext, expected_transcripts, out_segments):
    base_output = 'tests/good'
    convert('samples/invalid.stm', base_output + ext)
    validated_transcript = time_aligned_text(base_output + ext)
    assert len(validated_transcript.segments) == out_segments
    for seg, expected_text in zip(validated_transcript.segments, expected_transcripts):
        assert seg.text == expected_text


def test_stm_to_stm():
    " Test stm to stm validation "
    validate_sample('.stm', EXPECTED_UNFORMATTED_TRANSCRIPTS, 3)


def test_stm_to_json():
    " Test stm to gk json validation "
    validate_sample('.json', EXPECTED_FORMATTED_TRANSCRIPTS, 3)


def test_stm_to_vtt():
    " Test stm to vtt validation "
    validate_sample('.vtt', EXPECTED_FORMATTED_TRANSCRIPTS, 3)


def test_stm_to_html():
    " Test stm to html validation "
    validate_sample('.html', EXPECTED_FORMATTED_TRANSCRIPTS, 3)


def test_stm_to_srt():
    " Test stm to gk json validation "
    validate_sample('.srt', EXPECTED_FORMATTED_TRANSCRIPTS, 3)


def test_stm_to_txt():
    " Test stm to gk json validation "
    validate_sample('.txt', EXPECTED_FORMATTED_TRANSCRIPTS, 3)


if __name__ == "__main__":
    import sys
    import pytest

    pytest.main(sys.argv)
