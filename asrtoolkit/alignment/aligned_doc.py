#!/usr/bin/env python3

import logging
from collections import defaultdict, deque

import spacy
from toolz import merge, merge_sorted

from asrtoolkit.alignment.align_utils import find_matched_intervals, is_sorted

LOGGER = logging.getLogger(__name__)


class AlignedDoc:
    """
    An aligned document is an object that has two documents and a set of
    matched tokens and unmatched intervals between them

    hyp - should contain token time information
    ref - reference document; content is accurate

    """
    def __init__(self, hyp, ref, extractors, num_extractions=2):
        self.hyp = hyp
        self.ref = ref
        self.extractors = extractors

        self.matched_tokens = deque()
        self.matched_dict = defaultdict(dict)

        self.matched_intervals = deque()
        self.unmatched_intervals = deque()

        self.unmatched_intervals.append((self.hyp, self.ref))

        if not num_extractions:
            num_extractions = len(self.extractors)

        for extract_id in range(num_extractions):
            self.find_alignments(extract_id=extract_id)

    def add_extractors(self, extractors):
        """
        adds extractors List of Extractor object(s) to self.extractors
        """
        self.extractors.extend(extractors)

    def start_and_end_token(self, hyp, ref):
        """
        Return start and end token for spacy Doc,
        Span or Token part of self.hyp and self.ref
        """

        if isinstance(hyp, spacy.tokens.Doc) and isinstance(
                ref, spacy.tokens.Doc):
            hyp_start, hyp_end = hyp[0].i, hyp[-1].i
            ref_start, ref_end = ref[0].i, ref[-1].i

        elif isinstance(hyp, spacy.tokens.Token) and isinstance(
                ref, spacy.tokens.Token):
            hyp_start, hyp_end = hyp.i, hyp.i
            ref_start, ref_end = ref.i, ref.i
        else:
            hyp_start, hyp_end = hyp.start, hyp.end
            ref_start, ref_end = ref.start, ref.end
        return hyp_start, hyp_end, ref_start, ref_end

    def segment_to_tokens(self, segment):
        """
        segment: spacy Doc/Span/Token object
        returns list of token(s) comprising segment
        """
        if len(segment) > 1:
            return [tok for tok in segment]
        else:
            return [segment]  # is token

    def get_token_idxs(self, tokens):
        """tokens: List of one or more Token objects"""
        return [tok.i for tok in tokens]

    def _unique_matches(self, matched_segments):
        """
        matched_segments: List[span,span] as for matches_list
        :return:  each paired
        """
        assert isinstance(matched_segments, list)
        unique_new_spans = [
            match for match in matched_segments
            if match not in self.matched_intervals
        ]
        LOGGER.debug("Number of non-unique matched_segments: %s",
                     len(matched_segments) - len(unique_new_spans))
        return unique_new_spans

    def find_unmatched_segments(self, interval, matched_segments):
        """
        :param interval: doc/span -> unmatched_interval from which matched_segments were obtained (via extraction + sequence_matching)
        :param matched_segments: List[List[Span, Span]] -> List of Lists; inner Lists containing matching Spans from hyp and ref respectively; Spans are subsequences of text comprising hyp_segment and ref_segment of interval
        :return: List of List of Spans of Sequences of Text from Interval that were not matched
        """
        if not matched_segments:
            return

        unmatched_segments = []
        (hyp_segment, ref_segment) = interval

        for i in range(len(matched_segments[:-1])):
            m1, m2 = matched_segments[i]
            m1_next, m2_next = matched_segments[i + 1]
            slot1 = hyp_segment[m1.end + 1:m1_next.start]
            slot2 = ref_segment[m2.end + 1:m2_next.end]
            l = [slot1, slot2]
            LOGGER.debug(i, ":", l)

            if len(slot1) > 1 and len(slot2) > 1:
                unmatched_segments.append(l)

        # special cases
        # --> segment btw interval start and first match & last match and interval end
        hyp_start, hyp_end, ref_start, ref_end = self.start_and_end_token(
            hyp=hyp_segment, ref=ref_segment)

        m1_first, m2_first = matched_segments[0]
        if m1_first.start != hyp_start and m2_first.start != ref_start:
            slot1_first = hyp_segment[:m1_first.start]
            slot2_first = ref_segment[:m2_first.start]
            l = [slot1_first, slot2_first]

            if len(slot1_first) > 1 and len(slot2_first) > 1:
                unmatched_segments.insert(0, l)

        m1_last, m2_last = matched_segments[-1]
        if m1_last.end != hyp_end and m2_last.end != ref_end:
            slot1_last = hyp_segment[m1_last.end + 1:]
            slot2_last = ref_segment[m2_last.end + 1:]

            if len(slot1_last) > 1 and len(slot2_last) > 1:
                unmatched_segments.append(l)

        return unmatched_segments

    def find_alignments(self, extract_id):
        all_matched_segments, all_unmatched_segments = [], []

        for interval in self.unmatched_intervals:
            matched_segments = find_matched_intervals(
                interval=interval, extractor=self.extractors[extract_id])

            if matched_segments:
                all_matched_segments.extend(matched_segments)

                unmatched_segments = self.find_unmatched_segments(
                    interval=interval, matched_segments=matched_segments)
                for segment in (unmatched_segments
                                if unmatched_segments is not None else []):
                    all_unmatched_segments.append(segment)
            else:
                all_unmatched_segments.extend(
                    interval if hasattr(interval, "__iter__") else [interval])

        if all_matched_segments:
            # unmatched segments
            self.unmatched_intervals.clear()
            self.unmatched_intervals.extend(all_unmatched_segments)
            # matches
            self.matched_intervals.extend(all_matched_segments)

            # dict matches
            self.matched_dict[extract_id] = all_matched_segments

    def get_token_matches(self):
        """
        retrieves all matched intervals;
        verifies each paired span contains the same text
        decomposes to paired tokens - removes duplicates in the process
        :param aligned_doc:
        :return: List[Tuple[int,int]]
          ints -> token position in respective docs
            hyp[hyp_token].i, ref[ref_token].i
        """

        x = list(merge_sorted(self.matched_dict[0], self.matched_dict[1]))
        y = list(merge_sorted(x, self.matched_dict[2]))
        z = list(merge_sorted(y, self.matched_dict[3]))

        matched_spans = z

        token_matches = []
        for hyp_match, ref_match in matched_spans:
            assert hyp_match.text == ref_match.text
            m1_tokens = self.get_token_idxs(hyp_match)
            m2_tokens = self.get_token_idxs(ref_match)
            for hyp_tok, ref_tok in zip(m1_tokens, m2_tokens):
                matched = (hyp_tok, ref_tok)
                if matched not in token_matches and is_sorted(token_matches +
                                                              [matched]):
                    token_matches.append(matched)
        return token_matches

    def unique_token_matches(self):
        """
        converts token_matches (List of Tuples of Ints-> aligned token ids) TO Dict
        then convert back (List[Tuple[int,int]] --> ensures tuples are unique
          and both hyp and ref tokens are sorted
        """
        token_mapper = defaultdict(dict)
        token_matches = self.get_token_matches()

        for tok1, tok2 in sorted(token_matches):
            if tok1 not in token_mapper or abs(tok1 -
                                               token_mapper[tok1]) > abs(tok1 -
                                                                         tok2):
                token_mapper[tok1] = tok2
        return token_mapper

    def get_token_metadata(self):
        """
        given Tuples of matched token ids from hyp and ref -> self.get_token_matches()
          merges user_data corresponding to hyp (start_time/duration/end_time)
          and ref token of each pair (filename/speaker/gender) [requisite for STM file]
        :return: returns list of dicts with word-level information (merged from hyp and ref)
        """
        token_mapper = self.unique_token_matches()

        return [
            merge(self.hyp.user_data[d1_tok], self.ref.user_data[d2_tok])
            for d1_tok, d2_tok in token_mapper.items()
        ]
