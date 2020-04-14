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

from asrtoolkit.clean_formatting import clean_up
from asrtoolkit.data_structures.corpus import corpus

LOGGER = logging.getLogger(__name__)

def count_words(exemplar):
    """ Count words in a exemplar after cleaning it """
    return len(clean_up(exemplar.transcript_file.text()).split())


def generate_data_split(exemplars, words):
    """ Select exemplars to create data split with specified number of words """
    split_words = 0
    exemplars_in_split = []
    while split_words <= words:
        exemplars_in_split += [exemplars.pop(randrange(len(exemplars)))]
        split_words += exemplars_in_split[-1].n_words
    return exemplars_in_split, exemplars


def make_data_split(exemplars, out_dir):
   """ Move exemplars to a dev and test directory for corpus """
   for e in exemplars:
       os.rename(
           e.transcript_file.location,
           os.path.join(out_dir, os.path.basename(e.transcript_file.location))
       )
       os.rename(
           e.audio_file.location,
           os.path.join(out_dir, os.path.basename(e.audio_file.location))
       )


def split_corpus(in_dir, dev_dir='dev', dev_words=1000, tst_dir='test', test_words=1000, rand_seed=None, override=False):
    """
    Splits an ASR corpus directory based on number of words. At least 1000 words is recommended for each split.
    This means WER calculations are significant to about a tenth of a percent.
    Invalid files, such as empty files, will not be included in data splits.
    Set rand_seed for reproducible splits

    If you want more than 50% of the input data in dev and tests splits set override=True
    """
    seed(rand_seed)
    # Look in directory for all valid pairs of stm and audio file
    c = corpus({"location": in_dir})
    LOGGER.debug("%d exemplars before validating them", len(c.exemplars))
    valid_exemplars = [_ for _ in c.exemplars if _.validate()]
    LOGGER.debug("%d exemplars after validating them", len(valid_exemplars))
    # Count text from all valid stm files
  
    total_words = 0
    for e in valid_exemplars:
        e.n_words = count_words(e)
        total_words += e.n_words

    if dev_words + test_words > total_words:
        LOGGER.error(
            'Not enough words in corpus, %d, to split into groups %d and %d. Reduce words in data splits.',
            total_words,
            dev_words,
            test_words,
        )
        sys.exit(1)
    elif override or dev_words + test_words > 0.5 * total_words:
        LOGGER.error(
            "More than 50% of corpus words, %d, are being put into dev and tests splits (%d and %d). Set override=true if you still want to split",
            total_words,
            dev_words,
            test_words,
        )
        sys.exit(1)

    # Sample files to get enough words for corpus
    dev_exemplars, valid_exemplars = generate_data_split(valid_exemplars, dev_words)
    test_exemplars, _ = generate_data_split(valid_exemplars, test_words)

    LOGGER.info(
        'Making dev split with %d words using %d files',
        sum(map(lambda x: x.n_words, dev_exemplars)),
        len(dev_exemplars)
    )
    make_data_split(dev_exemplars, dev_dir)
    LOGGER.info(
        'Making test split with %d words using %d files',
        sum(map(lambda x: x.n_words, test_exemplars)),
        len(test_exemplars)
    )
    make_data_split(test_exemplars, tst_dir)

def cli():
    Fire(split_corpus)


if __name__ == "__main__":
    cli()
