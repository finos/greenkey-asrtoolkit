#!/usr/bin/env python
"""
Python function for computing the word diarization error rate for Automatic Speech Recognition files
following https://arxiv.org/pdf/1907.05337.pdf
"""

from collections import defaultdict

import rapidfuzz
from fire import Fire

from asrtoolkit.file_utils.script_input_validation import assign_if_valid


def get_words_and_index_mapping(transcript):
    loc = 0
    words = []
    word_idx_dict = {}
    for seg_idx, seg in enumerate(transcript.segments):
        word_list = seg.text.split()
        for idx, word in enumerate(word_list):
            words.append(word)
            word_idx_dict[loc + idx] = seg_idx
        loc += len(word_list)
    return words, word_idx_dict


def calculate_speaker_duration(transcript):
    """
    Calculate how much each speaker spoke

    Returns a dict of speaker: duration
    """
    return {
        speaker: sum(
            float(seg.stop) - float(seg.start)
            for seg in transcript.segments
            if seg.speaker == speaker
        )
        for speaker in set(seg.speaker for seg in transcript.segments)
    }


def segments_crosstalk(seg1, seg2):
    """
    Returns time of crosstalk between two segments
    """
    return max(
        0,
        min(float(seg2.stop), float(seg1.stop))
        - max(float(seg1.start), float(seg2.start)),
    )


def find_speaker_with_most_crosstalk(ref, hyp, target_ref_speaker):
    """
    For reference and hypothesis transcripts and a target speaker,
    return a dict of what speakers' in the hypothesis crosstalk the
    most with the target speaker
    """
    overlapping_speaker_duration = defaultdict(lambda: 0.0)

    target_speaker_segments = [
        seg for seg in ref.segments if seg.speaker == target_ref_speaker
    ]

    for seg in hyp.segments:
        overlapping_speaker_duration[seg.speaker] += sum(
            segments_crosstalk(seg, ref_seg) for ref_seg in target_speaker_segments
        )

    return dict(overlapping_speaker_duration)


def align_speaker_labels(ref, hyp):
    """
    Computes a mapping between reference (key) and hypothesis speakers
    by greedily assigning the speakers based on most prolific speakers
    """
    speaker_mapping = {}
    ref_speakers_with_time = calculate_speaker_duration(ref)
    for speaker, _ in sorted(
        ref_speakers_with_time.items(), key=lambda r: r[1], reverse=True
    ):
        overlapping_speakers = find_speaker_with_most_crosstalk(ref, hyp, speaker)
        speaker_mapping[speaker] = max(
            filter(lambda s: s not in speaker_mapping.values(), overlapping_speakers),
            default=None,
        )
    return speaker_mapping


def wder(ref, hyp, verbose=False, drop_crosstalk=False):
    """
    Computes the word diarization error rate for two files
    See https://arxiv.org/pdf/1907.05337.pdf
    For an example definition
    """

    ref_words, ref_word_idx_dict = get_words_and_index_mapping(ref)
    hyp_words, hyp_word_idx_dict = get_words_and_index_mapping(hyp)

    speaker_mapping = align_speaker_labels(ref, hyp)

    operations = rapidfuzz.distance.Levenshtein.opcodes(ref_words, hyp_words)
    s_is, c_is, s, c = 0, 0, 0, 0
    for operation in operations:
        if operation.tag == "equal":
            for ref_idx, hyp_idx in zip(
                range(operation.src_start, operation.src_end),
                range(operation.dest_start, operation.dest_end),
            ):
                ref_speaker = speaker_mapping[
                    ref.segments[ref_word_idx_dict[ref_idx]].speaker
                ]
                hyp_speaker = hyp.segments[hyp_word_idx_dict[hyp_idx]].speaker
                if drop_crosstalk and (
                    "crosstalk" in ref.segments[ref_word_idx_dict[ref_idx]].speaker
                    or "crosstalk" in hyp.segments[hyp_word_idx_dict[hyp_idx]].speaker
                ):
                    continue
                if ref_speaker == hyp_speaker:
                    c += 1
                else:
                    c_is += 1
        elif operation.tag == "replace":
            for ref_idx, hyp_idx in zip(
                range(operation.src_start, operation.src_end),
                range(operation.dest_start, operation.dest_end),
            ):
                ref_speaker = speaker_mapping[
                    ref.segments[ref_word_idx_dict[ref_idx]].speaker
                ]
                hyp_speaker = hyp.segments[hyp_word_idx_dict[hyp_idx]].speaker
                if drop_crosstalk and (
                    "crosstalk" in ref.segments[ref_word_idx_dict[ref_idx]].speaker
                    or "crosstalk" in hyp.segments[hyp_word_idx_dict[hyp_idx]].speaker
                ):
                    continue
                if ref_speaker == hyp_speaker:
                    s += 1
                else:
                    s_is += 1
    # return a dict of results if verbose=True
    return (
        {"c_is": c_is, "s_is": s_is, "s": s, "c": c}
        if verbose
        else 100 * (s_is + c_is) / max(1, (s + c))
    )


def compute_wder(
    reference_file,
    transcript_file,
    json_format=None,
    verbose=False,
    drop_crosstalk=False,
):
    """
    Compares a reference and transcript file and the calculates word diarization error rate (WER) between these two files
    """

    # read files from arguments
    ref = assign_if_valid(
        reference_file,
        file_format=json_format
        if json_format and reference_file.endswith(".json")
        else None,
    )
    hyp = assign_if_valid(
        transcript_file,
        file_format=json_format
        if json_format and transcript_file.endswith(".json")
        else None,
    )

    if ref is None or hyp is None:
        print(
            "Error with an input file. Please check all files exist and are accepted by ASRToolkit"
        )
    else:
        return wder(ref, hyp, verbose, drop_crosstalk=drop_crosstalk)


def cli():
    Fire(compute_wder)


if __name__ == "__main__":
    cli()
