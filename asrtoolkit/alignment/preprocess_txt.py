#!/usr/bin/env python3

import os
import logging

from asrtoolkit.clean_formatting import clean_up
LOGGER = logging.getLogger(__name__)


def parse_transcript(transcript,
                     speaker="unknown",
                     gender="male",
                     token_idx_offset=0):
    """
    Given reference transcript (and ideally speaker and gender),
    Return a list of tokenized word objects
    """

    if os.path.exists(transcript):
        transcript = open(transcript).read()
    else:
        LOGGER.info(
            "Transcript is not a file location; assuming it is raw text instead."
        )

    clean_lattice = []
    for i, token in enumerate(clean_up(transcript).split()):
        word_dict = dict(token=token,
                         token_idx=token_idx_offset + i,
                         speaker=speaker,
                         gender=gender)
        clean_lattice.append(word_dict)
    return clean_lattice
