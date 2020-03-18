#!/usr/bin/env python
"""
Module for holding information about an audio file and doing basic conversions
"""

import hashlib
import logging
import os
import subprocess

from asrtoolkit.file_utils.name_cleaners import (
    generate_segmented_file_name,
    sanitize_hyphens,
    strip_extension,
)
from asrtoolkit.file_utils.script_input_validation import valid_input_file
LOGGER = logging.getLogger()


def cut_utterance(source_audio_file,
                  target_audio_file,
                  start_time,
                  end_time,
                  sample_rate=16000):
    """
    source_audio_file: str, path to file
    target_audio_file: str, path to file
    start_time: float or str
    end_time: float or str
    sample_rate: int, default 16000; audio sample rate in Hz

    uses sox to segment source_audio_file to create target_audio_file that
    contains audio from start_time to end_time
        with audio sample rate set to sample_rate
    """
    subprocess.call(
        "sox -V1 {} -r {} -b 16 -c 1 {} trim {} ={}".format(
            source_audio_file,
            sample_rate,
            target_audio_file,
            start_time,
            end_time,
        ),
        shell=True,
    )


def degrade_audio(source_audio_file, target_audio_file=None):
    """
    Degrades audio to typical G711 level.
    Useful if models need to target this audio quality.
    """

    valid_input_file(source_audio_file, ["mp3", "sph", "wav", "au", "raw"])

    target_audio_file = (source_audio_file
                         if target_audio_file is None else target_audio_file)

    # degrade to 8k
    tmp1 = ".".join(source_audio_file.split(".")[:-1]) + "_tmp1.wav"
    subprocess.call(
        "sox -V1 {} -r 8000 -e a-law {}".format(source_audio_file, tmp1),
        shell=True,
    )

    # convert to u-law
    tmp2 = ".".join(source_audio_file.split(".")[:-1]) + "_tmp2.wav"
    subprocess.call(
        "sox -V1 {} --rate 8000 -e u-law {}".format(tmp1, tmp2),
        shell=True,
    )

    # upgrade to 16k a-law signed
    subprocess.call(
        "sox -V1 {} --rate 16000 -e signed  -b 16 --channel 1 {}".format(
            tmp2, target_audio_file),
        shell=True,
    )
    os.remove(tmp1)
    os.remove(tmp2)


def combine_audio(audio_files, output_file, gain=False):
    """
    Combine audio files with possible renormalization to 0dB
    """
    gain_str = ""
    if gain:
        gain_str = "gain -n 0"
    subprocess.call(
        "sox -V1 -m {} {} {}".format(" ".join(audio_files), output_file,
                                     gain_str),
        shell=True,
    )


class audio_file(object):
    """
    Create a audio_file object for
    - storing location
    - retrieving a unique hash
    - resampling for training
    - splitting into segments given an STM file
    """
    def __init__(self, location=""):
        """
        Populate file location info
        """
        self.location = None
        if not os.path.exists(location):
            raise FileNotFoundError(
                'Could not find file at "{}"'.format(location))
        self.location = location

    def hash(self):
        """
        Returns a sha1 hash of the file
        """
        if self.location:
            with open(self.location, "rb") as f:
                return hashlib.sha1(f.read()).hexdigest()
        else:
            return hashlib.sha1("".encode()).hexdigest()

    def prepare_for_training(self, file_name, sample_rate=16000):
        """
        Converts to single channel (from channel 1) audio file
        in SPH file format
        Returns audio_file object on success, else None
        """
        if file_name.split(".")[-1] != "sph":
            LOGGER.warning(
                "Forcing training data to use SPH file format for %s",
                file_name)
            file_name = strip_extension(file_name) + ".sph"

        file_name = sanitize_hyphens(file_name)

        # return None if error code given, otherwise return audio_file object
        output_file = (audio_file(file_name) if not subprocess.call(
            "sox -V1 {} {} rate {} remix -".format(self.location, file_name,
                                                   sample_rate),
            shell=True,
        ) else None)

        return output_file

    def split(self, transcript, target_dir):
        """
        Split audio file and transcript into many pieces based on
        valid segments of transcript
        """

        os.makedirs(target_dir, exist_ok=True)
        for iseg, seg in enumerate(transcript.segments):
            cut_utterance(
                self.location,
                generate_segmented_file_name(target_dir, self.location, iseg),
                seg.start,
                seg.stop,
            )
        transcript.split(target_dir)

        return
