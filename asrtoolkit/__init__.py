#!/usr/bin/env python3
import logging

from num2words import base
from pkg_resources import get_distribution

from .clean_formatting import clean_up
from .convert_transcript import convert
from .data_structures import (
    AudioFile,
    Corpus,
    Exemplar,
    Segment,
    Transcript,
    combine_audio,
)
from .file_utils.name_cleaners import basename, get_extension, sanitize, strip_extension
from .metrics import cer, get_words_and_index_mapping, tswde, wder, wer

LOGGER = logging.getLogger(__name__)

__version__ = get_distribution("asrtoolkit").version
__all__ = [
    AudioFile,
    base,
    basename,
    cer,
    clean_up,
    combine_audio,
    convert,
    Corpus,
    Exemplar,
    get_extension,
    sanitize,
    strip_extension,
    Transcript,
    wder,
    wer,
    tswde,
]
