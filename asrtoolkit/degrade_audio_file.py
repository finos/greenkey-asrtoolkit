#!/usr/bin/env python
"""
Script for degrading audio files to G711 audio quality
"""

import logging

from fire import Fire

from asrtoolkit.data_structures.audio_file import degrade_audio
from asrtoolkit.file_utils.script_input_validation import valid_input_file

LOGGER = logging.getLogger(__name__)


def degrade_all_files(*audio_files):
    """
    Degrade all audio files given as arguments (in place by default)
    """
    for file_name in audio_files:
        if valid_input_file(file_name, ["mp3", "sph", "wav", "au", "raw"]):
            degrade_audio(file_name)
        else:
            LOGGER.error("Invalid input file %s", file_name)


def cli():
    Fire(degrade_all_files)


if __name__ == "__main__":
    cli()
