#!/usr/bin/env python
"""
Module for reading/writing RTTM files

This expects a segment from class derived in convert_text

See https://catalog.ldc.upenn.edu/docs/LDC2004T12/RTTM-format-v13.pdf
for the RTTM file format standard, copied below with minor edits for clarity

RTTM files store object attributes in white-space separated fields

```
Field 1 2 3 4 5 6 7 8 9
type file chnl tbeg tdur ortho stype name conf
```
where
file is the waveform file base name (i.e., without path names or extensions).
chnl is the waveform channel (e.g., “1” or “2”).
tbeg is the beginning time of the object, in seconds, measured from the start time of the file. If there is no beginning time, use tbeg = “<NA>”.
tdur is the duration of the object, in seconds. If there is no duration, use tdur = “<NA>”.
stype is the subtype of the object. If there is no subtype, use stype = “<NA>”.
ortho is the orthographic rendering (spelling) of the object for STT object types. If there is no orthographic representation, use ortho = “<NA>”.
name is the name of the speaker. name must uniquely specify the speaker within the scope of the file. If name is not applicable or if no claim is being made as to the identity of the speaker, use name = “<NA>”.
conf is the confidence (probability) that the object information is correct. If conf is not available, use conf = “<NA>”.

"""

# do not delete - needed for time_aligned_text
from asrtoolkit.data_handlers.data_handlers_common import footer, separator
from asrtoolkit.data_structures import Segment
from asrtoolkit.data_structures.formatting import clean_float


def header():
    "Header for rttm files is empty"
    return ""


def format_segment(seg):
    """
    Formats a segment assuming it's an instance of class segment with elements
    filename, channel, speaker, start and stop times, label, and text
    """
    return f"SPEAKER {seg.filename} {seg.channel} {seg.start} {clean_float(float(seg.stop)-float(seg.start))} <NA> <NA> {seg.speaker} <NA> <NA>"


def read_file(file_name):
    """Reads an RTTM file"""

    segments = []
    with open(file_name) as data:
        for line in data:
            _, filename, channel, start, duration, _, _, speaker, _, _ = line.split()
            seg = Segment(
                **dict(
                    filename=filename,
                    channel=channel,
                    start=start,
                    stop=start + duration,
                    speaker=speaker,
                )
            )
            segments.append(seg)
    return segments


__all__ = [header, footer, separator]
