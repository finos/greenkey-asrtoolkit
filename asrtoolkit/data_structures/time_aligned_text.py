#!/usr/bin/env python
"""
Class for holding time_aligned text
"""

import hashlib
import importlib
import os

from asrtoolkit.file_utils.name_cleaners import (
    generate_segmented_file_name,
    sanitize_hyphens,
)


class Transcript:
    """
    Class for storing time-aligned text and converting between formats
    """

    location = ""
    segments = []
    file_extension = None

    def __init__(self, input_data=None, file_format=None):
        """
        Instantiates a time_aligned text object
        If 'input_data' is a string, it tries to find the appropriate file.

        >>> transcript = Transcript()
        """
        if (
            input_data is not None
            and isinstance(input_data, str)
            and os.path.exists(input_data)
        ):
            self.read(input_data, file_format)
        elif input_data is not None and type(input_data) in [str, dict]:
            self.file_extension = "txt" if isinstance(input_data, str) else "json"
            data_handler = importlib.import_module(
                "asrtoolkit.data_handlers.{:}".format(
                    file_format if file_format is not None else self.file_extension
                )
            )
            self.segments = list(filter(lambda seg: seg is not None, data_handler.read_in_memory(input_data)))

    def hash(self):
        """
        Returns a sha1 hash of the file
        """
        if self.location:
            with open(self.location) as f:
                return hashlib.sha1(f.read().encode()).hexdigest()
        else:
            return hashlib.sha1("".encode()).hexdigest()

    def __str__(self):
        """
        Returns string representation of formatted segments as corresponding
        By default, use the extension of the file you loaded
        >>> transcript = Transcript()
        >>> print(transcript.__str__()=="")
        True
        """
        data_handler = importlib.import_module(
            "asrtoolkit.data_handlers.{:}".format(
                self.file_extension if self.file_extension else "txt"
            )
        )
        return "\n".join(_.__str__(data_handler) for _ in self.segments)

    def __add__(self, other):
        """
        Add two transcripts
        Set the location after adding if you want to save this!
        """
        new_segments = self.segments + other.segments

        # Sort the segments by their start time then stop time
        new_segments.sort(key=lambda s: (float(s.start), float(s.stop)))

        out_transcript = Transcript()
        out_transcript.file_extension = self.file_extension
        out_transcript.segments = new_segments
        return out_transcript

    def text(self):
        """
        Returns unformatted text from all segments
        """
        data_handler = importlib.import_module(
            "asrtoolkit.data_handlers.{:}".format("txt")
        )
        return " ".join(_.__str__(data_handler) for _ in self.segments)

    def read(self, file_name, file_format=None):
        """Read a file using class-specific read function"""
        self.file_extension = file_name.split(".")[-1]
        self.location = file_name
        data_handler = importlib.import_module(
            "asrtoolkit.data_handlers.{:}".format(
                file_format if file_format is not None else self.file_extension
            )
        )
        self.segments = list(filter(lambda seg: seg is not None, data_handler.read_file(file_name)))

    def write(self, file_name, file_format=None):
        """
        Output to file using segment-specific __str__ function
        """
        file_extension = file_name.split(".")[-1] if "." in file_name else "stm"

        file_name = sanitize_hyphens(file_name)

        data_handler = importlib.import_module(
            "asrtoolkit.data_handlers.{:}".format(
                file_format if file_format else file_extension
            )
        )
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data_handler.header())
            f.writelines(
                data_handler.separator.join(
                    seg.__str__(data_handler) for seg in self.segments
                )
            )
            f.write(data_handler.footer())

        # return back new object in case we are updating a list in place
        return Transcript(file_name)

    def split(self, target_dir):
        """
        Split transcript into many pieces based on valid segments of transcript
        """
        os.makedirs(target_dir, exist_ok=True)
        for iseg, seg in enumerate(self.segments):
            new_seg = Transcript()
            new_seg.file_extension = self.file_extension
            new_seg.location = generate_segmented_file_name(
                target_dir, self.location, iseg
            )
            new_seg.segments = [seg]
            new_seg.write(new_seg.location)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
