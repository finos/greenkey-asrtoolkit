#!/usr/bin/env python
"""
Forced alignment tools CLI
"""

import argparse

from asrtoolkit.alignment import preprocess_gk_json, preprocess_txt
from asrtoolkit.alignment.align import align
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.name_cleaners import basename, sanitize, strip_extension


def align_json(ref_txt, json_file, filename=None):
    """
    Wraps alignment tools to allow for forced alignment of a gk json hypothesis against a reference text file
    Produces a time-aligned stm file named filename using the correct transcript where alignments were detected
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


def main():
    """
    CLI for forced alignment tools
    """
    parser = argparse.ArgumentParser(
        description="align a gk json file against a reference text file")
    parser.add_argument("input_json",
                        metavar="input_json",
                        type=str,
                        help="input gk json file")
    parser.add_argument("ref",
                        metavar="ref",
                        type=str,
                        help="reference text file")
    parser.add_argument("output_filename",
                        metavar="output_filename",
                        type=str,
                        default=None,
                        help="output_filename")

    args = parser.parse_args()
    align_gk_json(args.ref, args.input_json, args.output_filename)


if __name__ == "__main__":
    main()
