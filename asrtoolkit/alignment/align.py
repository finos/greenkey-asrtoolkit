#!/usr/bin/env python3

import logging

import en_core_web_sm

# Third Party
from spacy.tokens import Doc as spacy_doc
from textacy.extract import ngrams, noun_chunks
from toolz.sandbox.core import pluck

from asrtoolkit.alignment.align_utils import (
    Extractor,
    dict_to_segments,
    word_lattice_to_lines,
)
from asrtoolkit.alignment.aligned_doc import AlignedDoc

LOGGER = logging.getLogger(__name__)
NLP = en_core_web_sm.load()


class WhitespaceTokenizer:
    """
    Text (List of Tokens) to Spacy Docs
    Tokenizer input - list of words
      returned spacy Doc tokens same as initial word list
      equivalent to splitting on white space
    """
    def __init__(self, NLP):
        """NLP: loaded Spacy model"""
        self.vocab = NLP.vocab

    def __call__(self, word_list):
        """word_list: list of words; returns Doc"""
        return spacy_doc(self.vocab,
                         words=word_list,
                         spaces=[True] * len(word_list))


def init_spacy_document(
    lattice,
    token_key="token",
):
    """
    Given List of word-level dicts, initializes Spacy Doc
      using WhitespaceTokenizer
    :param: lattice: List[Dict];
      inner dicts contain token-level information for each token in input text
    :param: token_key: key in Dicts containing tokens in text
    :return: spacy Doc
      (1) text: ' '.join(dict['token'])
      (2) metadata: doc.user_data = lattice (word-level dicts)
        - Scribe output: word-level time offsets
        - reference transcript: speaker id and gender

    * Note: spacy model must be loaded and bound to NLP object
        NLP = spacy.load('en_core_web_sm')
    """
    NLP.make_doc = WhitespaceTokenizer(NLP)
    word_list = list(pluck(token_key, lattice))
    doc = NLP(word_list)
    doc.user_data = lattice
    assert len(doc) == len(
        word_list
    ), "document has different number of tokens {} from word_list {}".format(
        len(doc), len(word_list))
    return doc


def select_extractors(use_unigrams=False):
    """
    Extractors For Alignment
    :return: List of Extractors objects to use for text-text alignment
    note: ngram extractors below filter out stopwords and number words/symbols
    """
    noun_chunk_extractor = Extractor(
        lambda doc: list(filter(lambda x: len(x) > 3, list(noun_chunks(doc)))))
    tetragram_extractor = Extractor(
        lambda doc: list(ngrams(doc, 4, filter_stops=True, filter_nums=True)))
    trigram_extractor = Extractor(
        lambda doc: list(ngrams(doc, 3, filter_stops=True, filter_nums=True)))
    bigram_extractor = Extractor(lambda doc: list(
        ngrams(doc, 2, filter_stops=False, filter_nums=False)))
    unigram_extractor = Extractor(lambda doc: list(
        ngrams(doc, 1, filter_stops=False, filter_nums=False)))

    extractor_list = [
        noun_chunk_extractor,
        tetragram_extractor,
        trigram_extractor,
        bigram_extractor,
    ]

    if use_unigrams:
        extractor_list.append(unigram_extractor)

    return extractor_list


def lattices_to_aligned_doc(
    time_annotated_tokens,
    reference_tokens,
    extractors,
    num_extractions,
):
    """
    From two Lists of Word-Dicts, returns AlignedDoc (already aligned)
    :param time_annotated_tokens: List[Dict]; dicts with token-specific data
      including, at minimum, token start time and duration
    :param reference_tokens: List[Dict]; dicts with token-specific data
      including speaker(id) and gender
    :return: AlignedDoc object; contains
      end-product of text-text alignment and
      methods to retrieve matches with and without token-level metadata
    """
    # Create Spacy Docs from List of Tokens + Metadata
    hyp = init_spacy_document(lattice=time_annotated_tokens,
                              token_key="gk_token")
    ref = init_spacy_document(lattice=reference_tokens, token_key="token")
    return AlignedDoc(hyp, ref, extractors, num_extractions)


def get_segments_from_alignments(
    aligned_token_lattice,
    reference_doc,
    token_idx="token_idx",
    max_duration=15,
):
    """
    Uses Aligned Tokens to Segment Reference Text into STM Lines
    :param aligned_token_lattice: List of Dicts,STM
      each containing word-level information;
      all tokens are paired and contain data requisite for STM file
    :param max_duration: int; maximum duration of STM line audio
    :return: segments: List[Segment],
      each Segment object contains data for one STM Line
    """
    line_dict = word_lattice_to_lines(word_lattice=aligned_token_lattice,
                                      MAX_DURATION=max_duration)
    segments = dict_to_segments(line_dict=line_dict,
                                doc=reference_doc,
                                token_idx=token_idx)

    return line_dict, segments


def align(
    gk_json,
    ref_tokens,
    num_extractions=4,
    max_duration=15,
):
    """
    Given a gk_json and ref_tokens, apply extractors and align

    Using num_extractions extractors
    and aligning up to max_duration second segments
    """
    extractor_list = select_extractors()

    # Align data
    aligned_doc = lattices_to_aligned_doc(
        time_annotated_tokens=gk_json,
        reference_tokens=ref_tokens,
        extractors=extractor_list,
        num_extractions=num_extractions,
    )

    # combine hyp token metadata with aligned ref metadata
    token_lattice = aligned_doc.get_token_metadata()

    # dict & segment objects with lines under max_duration between matched tokens (w/ same speaker)
    line_dict, all_segments = get_segments_from_alignments(
        token_lattice,
        aligned_doc.ref,
        token_idx="token_idx",
        max_duration=max_duration,
    )

    min_duration = 3.0
    segments = [
        seg for seg in all_segments if seg.stop - seg.start > min_duration
    ]

    return segments
