#!/usr/bin/env python
"""
Forced alignment tools CLI
"""

from fire import Fire

from asrtoolkit.alignment import preprocess_gk_json, preprocess_txt
from asrtoolkit.alignment.align import align
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.name_cleaners import (
    basename,
    sanitize,
    strip_extension,
)


def align_json(ref_txt, json_file, filename=None):
    """
    CLI for forced alignment tools
    Using a reference txt file and a hypothesis gk json 
        file, this time-aligns the reference txt file 
        and outputs an STM file
    Input
      ref_txt, str - reference text file containing ground truth
      json_file, str - hypothesis gk JSON file
      filename, str - output STM filename
    """

    ref_tokens = preprocess_txt.parse_transcript(ref_txt)
    gk_json = preprocess_gk_json.preprocess_transcript(json_file)
    segments = align(gk_json, ref_tokens)

    if filename is None:
        filename = basename(sanitize(strip_extension(ref_txt))) + ".stm"

    # fix segment filename and speaker
    for seg in segments:
        seg.filename = strip_extension(filename)
        seg.speaker = strip_extension(filename) + "UnknownSpeaker"

    output = time_aligned_text()
    output.segments = segments
    output.write(filename)


def cli():
    Fire(align_json)


if __name__ == "__main__":
    cli()
