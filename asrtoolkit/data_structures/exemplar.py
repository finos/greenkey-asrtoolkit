#!/usr/bin/env python3

"""
Stores Exemplar class for corpus management
"""
import os

from asrtoolkit.clean_formatting import clean_up
from asrtoolkit.file_utils.name_cleaners import basename, strip_extension


class Exemplar:
    """
    Create an Exemplar class to pair one audio file with one transcript file
    """

    audio_file = None
    transcript_file = None

    def __init__(self, *args, **kwargs):
        "Instantiate using input args and kwargs"
        for dictionary in args:
            if isinstance(dictionary, dict):
                for key, value in dictionary.items():
                    setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def validate(self):
        """
        Validates Exemplar object by constraining that the filenames before the
        extension are the same
        """

        audio_filename = basename(strip_extension(self.audio_file.location))
        transcript_filename = basename(strip_extension(self.transcript_file.location))

        # Audio and transcript filename must match
        # Audio file must not be empty
        # Transcript file must not be empty
        valid = (
            audio_filename == transcript_filename
            and os.path.getsize(self.audio_file.location)
            and os.path.getsize(self.transcript_file.location)
        )
        # This returns an integer corresponding to the output of the last condition, not a boolean.
        # Thats just how `and` works in python

        return bool(valid)

    def count_words(self, clean_func=clean_up):
        """Count words in a Exemplar after cleaning it"""
        return (
            len(clean_func(self.transcript_file.text()).split())
            if self.validate()
            else 0
        )

    def prepare_for_training(self, target, sample_rate=16000, nested=False):
        """
        Prepare one Exemplar for training
        Returning a new Exemplar object with updated file locations
        and a resampled audio_file
        """
        if nested:
            af_target_file = os.path.join(
                target, "sph", basename(self.audio_file.location)
            )
            tf_target_file = os.path.join(
                target, "stm", basename(self.transcript_file.location)
            )
        else:
            af_target_file = os.path.join(target, basename(self.audio_file.location))
            tf_target_file = os.path.join(
                target, basename(self.transcript_file.location)
            )

        af = self.audio_file.prepare_for_training(
            af_target_file, sample_rate=sample_rate,
        )

        tf = self.transcript_file.write(tf_target_file)

        return (
            Exemplar({"audio_file": af, "transcript_file": tf})
            if all([af, tf])
            else None
        )

    def hash(self):
        """
        Returns combined hash of two files
        """
        return self.audio_file.hash() + self.transcript_file.hash()
