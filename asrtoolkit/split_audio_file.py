#!/usr/bin/env python
"""
Script for splitting audio files using a transcript with start/stop times
"""

import logging
import sys

from fire import Fire

from asrtoolkit.data_structures.audio_file import audio_file
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.script_input_validation import valid_input_file

LOGGER = logging.getLogger(__name__)


def split_audio_file(source_audio_file,
                     source_transcript,
                     target_directory="split"):
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
        LOGGER.error("Invalid transcript file %s", transcript)
        sys.exit(1)


def validate_audio_file(source_audio_file):
    if not valid_input_file(source_audio_file,
                            ["mp3", "sph", "wav", "au", "raw"]):
        LOGGER.error("Invalid audio file %s", source_audio_file)
        sys.exit(1)


def cli():
    Fire(split_audio_file)


if __name__ == "__main__":
    cli()
