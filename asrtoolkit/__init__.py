#!/usr/bin/env python3

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
from pkg_resources import get_distribution

__version__ = get_distribution("asrtoolkit").version
