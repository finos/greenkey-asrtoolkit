#!/usr/bin/env python3
import logging

from num2words import base
from pkg_resources import get_distribution

from asrtoolkit.clean_formatting import clean_up
from asrtoolkit.convert_transcript import convert
from asrtoolkit.data_structures.audio_file import audio_file, combine_audio
from asrtoolkit.data_structures.corpus import corpus
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.name_cleaners import (
    basename,
    get_extension,
    sanitize,
    strip_extension,
)
from asrtoolkit.wer import cer, wer

LOGGER = logging.getLogger(__name__)

__version__ = get_distribution("asrtoolkit").version
__all__ = [
    audio_file,
    base,
    basename,
    cer,
    clean_up,
    combine_audio,
    convert,
    corpus,
    get_extension,
    sanitize,
    strip_extension,
    time_aligned_text,
    wer,
]

try:
    from asrtoolkit.align_json import align_json

    __all__.append(align_json)
except ImportError:
    # Catch attribute error to lest doctests pass
    LOGGER.info(
        "Unable to import alignment utilities due to missing development package requirements"
    )
