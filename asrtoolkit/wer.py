#!/usr/bin/env python
"""
Python function for computing word error rates metric for Automatic Speech Recognition files
"""

import re

import editdistance
from fire import Fire

from asrtoolkit.clean_formatting import clean_up
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.script_input_validation import assign_if_valid

# defines global regex for tagged noises and silence
re_tagged_nonspeech = re.compile(r"[\[<][A-Za-z #]*[\]>]")

# define tokenization approach to handle spaces, tabs, and other space characters
tokenization = re.compile(r"\s+")

# defines global regex to remove these nsns
nonsilence_noises = [
    "noise",
    "um",
    "ah",
    "er",
    "umm",
    "uh",
    "mm",
    "mn",
    "mhm",
    "mnh",
    "huh",
    "hmm",
]
re_nonsilence_noises = re.compile(r"\b({})\b".format(
    "|".join(nonsilence_noises)))


def remove_nonsilence_noises(input_text):
    """
    Removes nonsilence noises from a transcript
    """
    return re.sub(re_nonsilence_noises, "", input_text)


def get_wer_components(ref_string, hyp_string):
    """
    Helper function that takes as input a reference string and a hypothesis string.
    Splits the strings by space, computes the WER formula numerator and denominator
    and returns both.

    >>> get_wer_components("this is a cat", "this is a dog")
    (1, 4)
    >>> get_wer_components(['a','b','c'], ['a','b','d'])
    (1, 3)
    """

    # apply tokenization if given as a string
    ref = tokenization.split(ref_string) if isinstance(ref_string,
                                                       str) else ref_string
    hyp = tokenization.split(hyp_string) if isinstance(hyp_string,
                                                       str) else hyp_string

    WER_numerator = editdistance.eval(ref, hyp)
    WER_denominator = max(1, len(ref))

    return WER_numerator, WER_denominator


def standardize_transcript(input_transcript, remove_nsns=False):
    """
    Given an input transcript or time_aligned_text object,
    remove non-speech events
    [optionally] remove non-silence noises

    >>> standardize_transcript("this is a test")
    'this is a test'
    >>> standardize_transcript("this is um a test")
    'this is um a test'
    >>> standardize_transcript("this is um a test", remove_nsns=True)
    'this is a test'
    """

    # accept time_aligned_text objects but use their output text
    input_transcript = (input_transcript.text() if isinstance(
        input_transcript, time_aligned_text) else input_transcript)

    # remove tagged noises and other non-speech events
    input_transcript = re.sub(re_tagged_nonspeech, " ", input_transcript)

    if remove_nsns:
        input_transcript = remove_nonsilence_noises(input_transcript)

    # clean punctuation, etc.
    input_transcript = clean_up(input_transcript)

    return input_transcript


def wer(ref, hyp, remove_nsns=False):
    """
    Calculate word error rate between two string or time_aligned_text objects
    >>> wer("this is a cat", "this is a dog")
    25.0
    """

    # standardize input string
    ref, hyp = map(lambda t: standardize_transcript(t, remove_nsns),
                   (ref, hyp))

    # calculate WER with helper function
    WER_numerator, WER_denominator = get_wer_components(ref, hyp)

    return 100 * WER_numerator / WER_denominator


def cer(ref, hyp, remove_nsns=False):
    """
    Calculate character error rate between two strings or time_aligned_text objects
    >>> cer("this cat", "this bad")
    25.0
    """

    # standardize and convert string to a list of characters
    ref, hyp = map(
        list,
        map(
            lambda transcript: standardize_transcript(transcript, remove_nsns),
            (ref, hyp),
        ),
    )

    # calculate CER with helper function
    CER_numerator, CER_denominator = get_wer_components(ref, hyp)

    return 100 * CER_numerator / CER_denominator


def compute_wer(reference_file,
                transcript_file,
                char_level=False,
                ignore_nsns=False):
    """
    Compares a reference and transcript file and calculates word error rate (WER) between these two files
    If --char-level is given, compute CER instead
    If --ignore-nsns is given, ignore non silence noises
    """

    # read files from arguments
    ref = assign_if_valid(reference_file)
    hyp = assign_if_valid(transcript_file)

    if ref is None or hyp is None:
        print(
            "Error with an input file. Please check all files exist and are accepted by ASRToolkit"
        )
    elif char_level:
        print("CER: {:5.3f}%".format(cer(ref, hyp, ignore_nsns)))
    else:
        print("WER: {:5.3f}%".format(wer(ref, hyp, ignore_nsns)))


def cli():
    Fire(compute_wer)


if __name__ == "__main__":
    cli()
