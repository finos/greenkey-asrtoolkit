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


def log_corpus_creation(corpus, name):
    """ had to make this function to satisfy code climate """
    LOGGER.info(
        'Created %s split with %d words using %d files',
        corpus.location,
        sum(map(lambda x: x.n_words, corpus.exemplars)),
        len(corpus.exemplars)
    )


def split_corpus(in_dir, split_dir, split_name='split', split_words=1000, leftover_data_split_name='orig', rand_seed=None):
    """
    Splits an ASR corpus directory based on number of words outputting splits in split_dir.
    At least 1000 words is recommended for dev or tests splits to make WER calculations significant ~0.1%
    Invalid files, such as empty files, will not be included in data splits.

    Set rand_seed for reproducible splits
    """
    seed(rand_seed)

    c = corpus({"location": in_dir})
    LOGGER.debug("%d exemplars before validating them", len(c.exemplars))
    valid_exemplars = [_ for _ in c.exemplars if _.validate()]
    c.exemplars = valid_exemplars
    LOGGER.debug("%d exemplars after validating them", len(valid_exemplars))

    total_words = 0
    for e in valid_exemplars:
        e.n_words = e.count_words()
        total_words += e.n_words

    if split_words > total_words:
        LOGGER.error(
            'Not enough words in corpus, %d, to make a split with %d words. Reduce words in data split.',
            total_words,
            split_words,
        )
        sys.exit(1)

    leftover_corpus, new_corpus = c.split(split_words)

    new_corpus.prepare_for_training(os.path.join(split_dir, split_name))
    log_corpus_creation(new_corpus, split_name)

    leftover_corpus.prepare_for_training(os.path.join(split_dir, leftover_data_split_name))
    log_corpus_creation(leftover_corpus, leftover_data_split_name)


def cli():
    Fire(split_corpus)


if __name__ == "__main__":
    cli()
