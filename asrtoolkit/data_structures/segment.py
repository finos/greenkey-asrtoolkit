#!/usr/bin/env python3
"""
Class for holding a segment

"""
import json
import logging

from asrtoolkit.data_structures.formatting import clean_float

LOGGER = logging.getLogger(__name__)


class segment(object):
    """
    Class for holding segment-specific information
    Segment objects corresponds to dict under the key 'segment'
    in the ASR generated transcript (lattice)
    - the fields included below are shared across 'segments'
      but 'segments' may contain many other fields (i.e. sentiment) depending
      on the the text processing pipeline selected.
    """

    # refer to some file if possible
    filename = "unknown"
    # by default, use channel 1
    channel = "1"
    # need a speaker id
    speaker = "UnknownSpeaker"
    # start at beginning of file
    start = clean_float(0.0)
    # this should go the length of the file or the segment
    stop = clean_float(0.0)

    # Arbitrarily choose a default gender since
    # unknown does not play well with some programs
    # which digest ASR output
    label = "<o,f0,male>"
    # text to be populated from read class
    text = ""
    # text for printing out to fancy output formats
    formatted_text = ""
    # confidence in accuracy of text
    confidence = 1.0

    def __init__(self, *args, **kwargs):
        """
        Stores and initializes filename, channel, speaker, start & stop times,
        label, and formatted and unformatted text fields.
        - Unmodified ASR transcripts are unformatted text.
        - Raw Chat data is formatted text;
          `clean_up` from asrtoolkit.clean_formatting is used to
          convert it to unformatted text
        Note: `channel` (as currently defined) applies only to audio input
          - all chat data will retain default value of '1'

        >>> seg = segment({"text":"this is a test"})

        """
        for dictionary in [_ for _ in args if isinstance(_, dict)]:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self, data_handler=None):
        """
        Returns the string corresponding to TXT format by default
        >>> seg = segment({"text":"this is a test"})
        >>> print(seg)
        this is a test
        """
        ret_str = data_handler.format_segment(
            self) if data_handler else self.text

        return ret_str

    def validate(self):
        """
        Checks for common failure cases for if a line is valid or not
        """
        valid = (self.speaker != "inter_segment_gap" and self.text
                 and self.text != "ignore_time_segment_in_scoring"
                 and self.label in ["<o,f0,male>", "<o,f0,female>"])

        try:
            self.start = clean_float(self.start)
            self.stop = clean_float(self.stop)
        except Exception as exc:
            valid = False
            print(exc)

        if not valid:
            LOGGER.error(
                """Skipping segment due to validation error.
Please note that this invalidates WER calculations based on the entire file.
Segment: %s""",
                json.dumps(self.__dict__),
            )

        if "-" in self.filename:
            self.filename = self.filename.replace("-", "_")
            print(
                "Please rename audio file to replace hyphens with underscores")

        return valid


if __name__ == "__main__":
    import doctest

    doctest.testmod(raise_on_error=True, verbose=True)
