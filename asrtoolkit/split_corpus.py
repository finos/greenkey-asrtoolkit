#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create train, dev, and test splits a folder of ASR data
"""

import logging
import os
import sys
from random import seed, randrange

from fire import Fire

from asrtoolkit.data_structures.corpus import corpus

LOGGER = logging.getLogger(__name__)


def log_corpus_creation(corp, name):
    """ had to make this function to satisfy code climate """
    LOGGER.info(
        'Created %s split with %d words using %d files with %d segments',
        corp.location,
        sum(map(lambda x: x.n_words, corp.exemplars)),
        len(corp.exemplars),
        corp.calculate_number_of_segments()
    )


def perform_split(corpus_to_split, split_dir, split_name, split_words, min_split_segs, leftover_data_split_name):
    leftover_corpus, new_corpus = corpus_to_split.split(split_words, min_split_segs)

    new_corpus.prepare_for_training(os.path.join(split_dir, split_name))
    log_corpus_creation(new_corpus, split_name)

    leftover_corpus.prepare_for_training(os.path.join(split_dir, leftover_data_split_name))
    log_corpus_creation(leftover_corpus, leftover_data_split_name)


def split_corpus(in_dir, split_dir, split_name='split', split_words=1000, min_split_segs=10, leftover_data_split_name='orig', rand_seed=None):
    """
    Splits an ASR corpus directory based on number of words outputting splits in split_dir.
    At least 1000 words is recommended for dev or tests splits to make WER calculations significant ~0.1%
    Invalid files, such as empty files, will not be included in data splits.

    Set rand_seed for reproducible splits
    """
    seed(rand_seed)

    c = corpus({"location": in_dir})
    LOGGER.debug("%d exemplars before validating them", len(c.exemplars))
    valid_exemplars, total_words = c.count_exemplar_words()
    c.exemplars = valid_exemplars
    LOGGER.debug("%d exemplars after validating them", len(valid_exemplars))

    if min_split_segs > c.calculate_number_of_segments():
        LOGGER.error(
            'Not enough valid segments in corpus, %d, to make a split with %d segments. Reduce min_split_segs or get more data',
            c.calculate_number_of_segments(),
            min_split_segs,
        )
        sys.exit(1)

    perform_split(c, split_dir, split_name, split_words, min_split_segs, leftover_data_split_name)


def cli():
    Fire(split_corpus)


if __name__ == "__main__":
    cli()
