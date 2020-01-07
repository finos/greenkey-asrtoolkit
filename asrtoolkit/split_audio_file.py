#!/usr/bin/env python
"""
Script for splitting audio files using a transcript with start/stop times
"""

import argparse
import logging
import sys

from asrtoolkit.data_structures.audio_file import audio_file
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.script_input_validation import valid_input_file

LOGGER = logging.getLogger(__name__)


def split_audio_file(source_audio_file, source_transcript, target_directory):
    """
    Split source audio file into segments denoted by transcript file
    into target_directory
    Results in stm and sph files in target directory
    """
    source_audio = audio_file(source_audio_file)
    transcript = time_aligned_text(source_transcript)
    source_audio.split(transcript, target_directory)


def validate_transcript(transcript):
    """
    Exit if invalid transcript
    """
    if not valid_input_file(transcript):
        LOGGER.error("Invalid transcript file {}".format(transcript))
        sys.exit(1)


def validate_audio_file(source_audio_file):
    if not valid_input_file(source_audio_file,
                            ["mp3", "sph", "wav", "au", "raw"]):
        LOGGER.error("Invalid audio file {}".format(source_audio_file))
        sys.exit(1)


def main():
    """
    Split audio file using transcript file
    """
    parser = argparse.ArgumentParser(
        description=
        "Split an audio file using valid segments from a transcript file. For this utility, transcript files must contain start/stop times."
    )
    parser.add_argument("--target-dir",
                        default="split",
                        required=False,
                        help="Path to target directory")
    parser.add_argument("audio_file",
                        metavar="audio_file",
                        type=str,
                        help="input audio file")
    parser.add_argument("transcript",
                        metavar="transcript",
                        type=str,
                        help="transcript")

    args = parser.parse_args()

    split_audio_file(args.audio_file, args.transcript, args.target_dir)


if __name__ == "__main__":
    main()
