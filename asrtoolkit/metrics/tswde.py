#!/usr/bin/env python
"""
Python function for computing target speaker word diarization error statistics
"""


from collections import defaultdict

import rapidfuzz
from fire import Fire

from asrtoolkit.file_utils.script_input_validation import assign_if_valid

from .wder import get_words_and_index_mapping


def tswde(
    ref, hyp, target_speaker, beta=1.0, include_deletions=True, include_insertions=True
):
    """
    Computes target speaker word diarization error statistics

    Inspired by the word diarization error rate

    Returns f-score, precision, and recall for the assignment of words to speakers
    for a given target speaker as compared to all other speakers
    """

    ref_words, ref_word_idx_dict = get_words_and_index_mapping(ref)
    hyp_words, hyp_word_idx_dict = get_words_and_index_mapping(hyp)

    operations = rapidfuzz.distance.Levenshtein.opcodes(ref_words, hyp_words)
    true_positives, false_positives, true_negatives, false_negatives = 0, 0, 0, 0
    other = "other"
    speaker_mapping = defaultdict(lambda: other)
    speaker_mapping[target_speaker] = target_speaker
    for operation in operations:
        if operation.tag in {"equal", "replace"}:
            for ref_idx, hyp_idx in zip(
                range(operation.src_start, operation.src_end),
                range(operation.dest_start, operation.dest_end),
            ):
                ref_speaker = speaker_mapping[
                    ref.segments[ref_word_idx_dict[ref_idx]].speaker
                ]

                hyp_speaker = speaker_mapping[
                    hyp.segments[hyp_word_idx_dict[hyp_idx]].speaker
                ]

                # words which belong to the officer are attributed to the officer
                true_positives += ref_speaker == hyp_speaker == target_speaker

                # words which belong to non-officer are attributed to the officer
                false_positives += (
                    hyp_speaker == target_speaker and ref_speaker == other
                )

                # words which belong to non-officer are attributed to the non-officer
                true_negatives += ref_speaker == hyp_speaker == other

                # words which belong to officer are attributed to the non-officer
                false_negatives += (
                    ref_speaker == target_speaker and hyp_speaker == other
                )
        elif operation.tag == "delete" and include_deletions:
            for idx in range(operation.src_start, operation.src_end):
                ref_speaker = speaker_mapping[
                    ref.segments[ref_word_idx_dict[idx]].speaker
                ]
                # words which belong to officer are attributed to the non-officer
                false_negatives += ref_speaker == target_speaker

        elif operation.tag == "insert" and include_insertions:
            for idx in range(operation.dest_start, operation.dest_end):
                hyp_speaker = speaker_mapping[
                    hyp.segments[hyp_word_idx_dict[idx]].speaker
                ]
                # words which belong to non-officer are attributed to the officer
                false_positives += hyp_speaker == target_speaker

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    fscore = (1 + beta**2) * (precision * recall) / ((beta**2 * precision) + recall)

    return {"fscore": fscore, "precision": precision, "recall": recall}


def compute_tswde(reference_file, transcript_file, target_speaker, json_format=None):
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
        return tswde(ref, hyp, target_speaker)


def cli():
    Fire(compute_tswde)


if __name__ == "__main__":
    cli()
