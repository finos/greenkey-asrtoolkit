#!/usr/bin/env python3

import itertools
import logging
from collections import defaultdict

from asrtoolkit.data_structures.segment import segment as Segment
from toolz import merge

from asrtoolkit.alignment.initialize_logger import initialize_logger

initialize_logger()
LOGGER = logging.getLogger(__name__)

from toolz.sandbox.core import pluck


class Extractor:
    def __init__(self, extractor_function):
        self.extractor_function = extractor_function

    def match_extractions(self, extract1, extract2):
        """
        :param gk_extract: list of spacy/textacy Spans
        :param stm_extract: list of spacy/textacy Spans
        :return: 2 lists of spans, gk_shared and stm_shared, each with all spans in gk_extract and stm_extract, respectively,
          if the text (span.text) appears in both input lists
          gk_shared and stm_shared may differ in size and in order of elements contained
            but sorted(set(gk_shared))==sorted(set(stm_shared))   # where sorted uses text of each span
        """
        shared = set(x.text for x in extract1).intersection(
            set(x.text for x in extract2))
        extract1_shared = [x for x in extract1 if x.text in shared]
        extract2_shared = [x for x in extract2 if x.text in shared]
        return extract1_shared, extract2_shared

    def shared_extractions(self, hyp, ref):
        """return: Tuple[List[Span], List[Span]]"""
        hyp_extracted = list(self.extractor_function(hyp))
        ref_extracted = list(self.extractor_function(ref))
        return self.match_extractions(hyp_extracted, ref_extracted)


##########################################################################


# Aligner Functions
def find_matched_intervals(interval, extractor):
    """
    :param interval: Tuple(Tuple(int,int),Tuple(int,int))
      tuple with 2 tuples
        inner tuples consist of 2 integers--> the first and last token index of a segment from hyp and ref, respectively

    :param extractor: Extractor object
    :return: List of Lists of (matched) Spans (if any)
      returns an empty list if no shared segments are extracted
      or if shared extractions are not matched
    """

    matched_list = []

    # If either is a token, do not try to look for matches
    try:
        if not (len(interval[0]) > 1 and len(interval[1]) > 1):
            return matched_list
    # token does not support indexing
    except TypeError as exc:
        LOGGER.info("Error with %s: %s", interval, exc)
        return matched_list

    try:
        shared_extractions = extractor.shared_extractions(
            interval[0], interval[1])
    except TypeError as exc:
        LOGGER.info("Error with %s: %s", interval, exc)
        return

    if not shared_extractions[0] or not shared_extractions[1]:
        return
    else:
        gk_shared, ref_shared = shared_extractions
        matched_list = sequence_match(gk_shared, ref_shared)
    return matched_list


def is_sorted(token_matches):
    # verify in order
    hyp_tokens = list(pluck(0, token_matches))
    ref_tokens = list(pluck(1, token_matches))
    return sorted(hyp_tokens) == hyp_tokens and sorted(
        ref_tokens) == ref_tokens


def overlap_tokens(doc, other_doc):
    """
    Get the tokens from the original Doc that are also in the comparison Doc.
    """
    overlap = []
    other_tokens = [token.text for token in other_doc]
    for token in doc:
        if token.text in other_tokens:
            other_id = other_tokens.index(token.text)
            overlap.append([token, other_doc[other_id]])
    return overlap


def sequence_match(gk_shared, stm_shared):  # -> List[Tuple[Span, Span]]
    """
    :param: gk_shared: list of Spans
    :param: stm_shared: list of Spans
    Spans are obtained by applying an extractor to aligned segments of text from gk_doc and stm_doc
    and filtering results so each list only contains Spans with text present in at least one Span in the other segment
     - thus sorted(list(set([span.text for span in {doc}_shared])))-> same for doc=gk and doc=stm
     but the order and number of Spans in gk_shared and stm_shared may (and likely do) differ

    :return: list of tuples of spans  -> List[Tuple[Span, Span]]
        each tuple contains a matched pair from (gk_doc/segment, stm_doc/segment)
    """
    gk_text = [left.text for left in gk_shared]
    stm_text = [left.text for left in stm_shared]

    # Sequence Search
    matches_list = []
    still_left = []
    gk_taken_list = []

    for stm_item, stm_word in zip(stm_shared, stm_text):
        # gk_text: list of potential match spans
        if stm_word in gk_text:
            # get gk text match index
            match_idx = gk_text.index(stm_word)

            # use to get spacy item match -> gk_left = gk_shared
            # indexing into spacy objects list
            gk_item = gk_shared[match_idx]

            if not matches_list:  # first match
                matches_list.append([gk_item, stm_item])
                gk_taken_list.append(gk_item)

            elif gk_item not in gk_taken_list:  # not already matched
                prev_gk, prev_stm = matches_list[-1]  # get previous match

                # add to matches if token position of current matched gk & stm spans later than last
                if (prev_gk[0].idx < gk_item[0].idx
                        and prev_stm[0].idx < stm_item[0].idx):
                    matches_list.append([gk_item, stm_item])
                    gk_taken_list.append(gk_item)

                else:
                    # remove, add to still_left
                    popped = matches_list.pop()
                    still_left.append(popped)
    return matches_list


# Helper Functions
def flatten(embedded_iterable):
    return itertools.chain.from_iterable(embedded_iterable)


def merge_paired_dicts(dicts1, dicts2):
    """
    dicts1, dicts2: list of dicts of equal length -> List[Dict], List[Dict]
    :return: list with the same number of dicts as input dicts;
      dicts at the same index will be merged
        -> equivalent to dict1.update(dict2) for dicts at same index in dicts1 and dicts2
      all *unique* keys (& respective values) are retained
      if merged dicts contain the same key, only the value of key in dict1 will be retained

    merge only takes 2 arguments but dicts being merged can have multiple keys
    can NOT pass two lists of dicts
    """
    return [merge(dicts1, dicts2) for dicts1, dicts2 in zip(dicts1, dicts2)]


def stm_label(gender):
    return f"<o,f0,{gender}>"


def word_lattice_to_lines(word_lattice, MAX_DURATION=15):
    """
    :param word_lattice: List[Dict]
    dicts contain word-level information from transcribed document (start/end time)
    and reference document (filename, speaker, gender)

    # from tests.py : 10 tokens, one... nine; same for both (full match)
    lattice = merge_dicts(expected_gk_processed_output, expected_earnings_reference_output)

    :return: dict with keys: ints (stm line)
    values: Dict-word level information; all dicts with words, when combined are under
    MAX_DURATION and consist of a single speaker
    """
    line_dict = defaultdict(list)
    line_no = 0
    start_time, speaker_id = word_lattice[0]["start"], word_lattice[0][
        "speaker"]
    line_dict[line_no].append(word_lattice[0])
    for word_dict in word_lattice[1:]:
        if (word_dict["speaker"] != speaker_id
                or word_dict["end"] - start_time > MAX_DURATION):
            # start new line with new speaker and start time
            line_no += 1
            speaker_id, start_time = word_dict["speaker"], word_dict["start"]
            line_dict[line_no].append(word_dict)
        else:
            line_dict[line_no].append(word_dict)
    return line_dict


def dict_to_segments(line_dict, doc, token_idx="token_idx"):
    """Dict; key=int (stm line number); value: list of Dicts-> all word_dicts for tokens in line"""
    segments = []
    for group_key, group in line_dict.items():
        d = group[0]

        first_token_idx, last_token_idx = group[0][token_idx], group[-1][
            token_idx]
        text = doc[first_token_idx:last_token_idx + 1].text

        # fallback logic around speaker gender
        gender = d["gender"]
        if gender not in ["male", "female"]:
            gender = "male"
        segment = Segment(
            dict(
                channel=1,
                speaker=d["speaker"],
                start=d["start"],
                stop=group[-1]["end"],
                label=stm_label(gender),
                text=text,
            ))
        segments.append(segment)
    return segments
