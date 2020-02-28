#!/usr/bin/env python3

import json

from asrtoolkit.clean_formatting import clean_up


def preprocess_transcript(input_file):
    """
    Given a str file path to gk json output
    Return a list of tokenized word objects
    """
    data = json.load(open(input_file, "r+", encoding="utf-8"))
    segment_times = [(segment["startTimeSec"], segment["endTimeSec"])
                     for segment in data["segments"]]
    lattice_segments = [segment["words"] for segment in data["segments"]]
    transcript_segments = [
        segment["transcript"] for segment in data["segments"]
    ]

    # start token count (increment for included tokens)
    token_idx = 0
    clean_lattice = []
    changed = []
    for seg_id, seg_text in enumerate(transcript_segments):
        seg_lattice = lattice_segments[seg_id]
        start_time, end_time = segment_times[seg_id]
        for i, token in enumerate(seg_text.split()):
            clean_token = clean_up(token).strip()
            if clean_token:
                word_dict = seg_lattice[i]
                assert word_dict["word"] == token

                if word_dict["word"] != clean_token:
                    changed.append([seg_id, i, token, clean_token])

                # times (audio-aligned)
                start, duration = start_time + word_dict["start"], word_dict[
                    "length"]
                end = start + duration

                # generate token-level dict for each cleaned token retained
                word_dict = dict(
                    gk_token=clean_token,
                    gk_token_idx=token_idx,
                    seg_id=seg_id,
                    start=start,
                    end=end,
                    duration=duration,
                )
                # adding cleaned word + metadata to clean_lattice
                clean_lattice.append(word_dict)
                token_idx += 1
    return clean_lattice
