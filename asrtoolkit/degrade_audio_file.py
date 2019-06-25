#!/usr/bin/env python
"""
Script for degrading audio files to G711 audio quality
"""

import sys
import logging
from asrtoolkit.data_structures.audio_file import degrade_audio
from asrtoolkit.file_utils.script_input_validation import valid_input_file

LOGGER = logging.getLogger(__name__)


def main():
    """
    Degrade all audio files given as arguments (in place by default)
    """
    for file_name in sys.argv[1:]:
        if valid_input_file(file_name, ["mp3", "sph", "wav", "au", "raw"]):
            degrade_audio(file_name)
        else:
            LOGGER.error("Invalid input file %s", file_name)


if __name__ == "__main__":
    main()
