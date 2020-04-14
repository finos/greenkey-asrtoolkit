#!/usr/bin/env python
"""
Test audio file splitter
"""
import os
import shutil
from os.path import join as pjoin

from asrtoolkit.split_corpus import split_corpus


def setup_test_corpus(trn_dir, dev_dir, tst_dir):
    """ Setup fake corpus for testing """
    os.makedirs(trn_dir, exist_ok=True)
    os.makedirs(dev_dir, exist_ok=True)
    os.makedirs(tst_dir, exist_ok=True)
    n_files = 10
    for i in range(n_files):
        # "Convert" to sph becuase corpus expects that format and test doesn't read audio files
        shutil.copy("tests/small-test-file.mp3", pjoin(trn_dir, "file-{:02d}.sph".format(i)))
        shutil.copy("tests/small-test-file.stm", pjoin(trn_dir, "file-{:02d}.stm".format(i)))


def validate_split(directory, inds):
    """ Validate the files were split as expected """
    assert set(os.listdir(directory)) == {
        "file-{:02d}.{}".format(i, ext)
        for ext in ['sph', 'stm']
        for i in inds
    }


def test_split_corpus():
    """ Test corpus splitter """
    corpus_dir = "tests/split-corpus"

    trn_dir = pjoin(corpus_dir, "train")
    dev_dir = pjoin(corpus_dir, "dev")
    tst_dir = pjoin(corpus_dir, "test")

    setup_test_corpus(trn_dir, dev_dir, tst_dir)
    split_corpus(trn_dir, dev_dir=dev_dir, dev_words=19, tst_dir=tst_dir, test_words=19, rand_seed=1337)
    validate_split(trn_dir, [0, 1, 3, 4, 7, 9])
    validate_split(dev_dir, [5, 6])
    validate_split(tst_dir, [2, 8])


if __name__ == "__main__":
    import sys
    import pytest

    pytest.main(sys.argv)
