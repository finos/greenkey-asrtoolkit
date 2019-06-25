#!/usr/bin/env python
"""
Script for splitting audio files using a transcript with start/stop times
"""

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.data_structures.audio_file import audio_file
from asrtoolkit.file_utils.script_input_validation import valid_input_file

import argparse
import logging

LOGGER = logging.getLogger(__name__)


def main():
    """
    Split audio file using transcript file
    """
    parser = argparse.ArgumentParser(
        description=
        "Split an audio file using valid segments from a transcript file. For this utility, transcript files must contain start/stop times."
    )
    parser.add_argument('--target-dir',
                        default='split',
                        required=False,
                        help="Path to target directory")
    parser.add_argument('audio_file',
                        metavar='audio_file',
                        type=str,
                        help='input audio file')
    parser.add_argument('transcript',
                        metavar='transcript',
                        type=str,
                        help='transcript')

    args = parser.parse_args()

    if valid_input_file(args.transcript):
        transcript = time_aligned_text(args.transcript)
    else:
        LOGGER.error("Invalid transcript file {}".format(args.transcript))

    if valid_input_file(args.audio_file, ["mp3", "sph", "wav", "au", "raw"]):
        source_audio = audio_file(args.audio_file)
    else:
        LOGGER.error("Invalid audio file {}".format(args.audio_file))

    source_audio.split(transcript, args.target_dir)


if __name__ == "__main__":
    main()
