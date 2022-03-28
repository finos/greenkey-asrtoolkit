#!/usr/bin/env python
"""
Test audio file splitter
"""
import os
import shutil
from os.path import join as pjoin

from utils import get_sample_dir, get_test_dir

from asrtoolkit.data_structures import Corpus
from asrtoolkit.split_corpus import split_corpus

test_dir = get_test_dir(__file__)
sample_dir = get_sample_dir(__file__)


def setup_test_corpus(orig_dir, trn_dir, dev_dir, n_exemplars):
    """Setup fake corpus for testing"""
    os.makedirs(orig_dir, exist_ok=True)
    os.makedirs(trn_dir, exist_ok=True)
    os.makedirs(dev_dir, exist_ok=True)
    for i in range(n_exemplars):
        shutil.copy(
            f"{test_dir}/small-test-file.mp3",
            pjoin(orig_dir, "file-{:02d}.mp3".format(i)),
        )
        shutil.copy(
            f"{test_dir}/small-test-file.stm",
            pjoin(orig_dir, "file-{:02d}.stm".format(i)),
        )


def validate_split(directory, inds):
    """Validate the files were split as expected"""
    assert set(os.listdir(directory)) == {
        "file-{:02d}.{}".format(i, ext) for ext in ["sph", "stm"] for i in inds
    }


def test_split_corpus():
    """Test corpus splitter"""
    n_exemplars = 10
    corpus_dir = f"{test_dir}/split-corpus"

    orig_dir = pjoin(corpus_dir, "orig")
    split_dir = pjoin(corpus_dir, "splits")
    trn_dir = pjoin(split_dir, "train")
    dev_dir = pjoin(split_dir, "dev")

    setup_test_corpus(orig_dir, trn_dir, dev_dir, n_exemplars)
    orig_corpus = Corpus({"location": orig_dir})
    split_corpus(
        orig_dir,
        split_dir=split_dir,
        split_name="dev",
        split_words=19,
        min_split_segs=1,
        leftover_data_split_name="train",
        rand_seed=1337,
    )

    # Make sure we didn't destroy input data
    final_corpus = Corpus({"location": orig_dir})
    assert orig_corpus.validate() == 1
    assert final_corpus.validate() == 1
    orig_hashes = [_.hash() for _ in orig_corpus.exemplars]
    final_hashes = [_.hash() for _ in final_corpus.exemplars]
    assert all(h in final_hashes for h in orig_hashes)

    # Make sure correct number of words present in data split
    dev_corpus = Corpus({"location": dev_dir})
    assert sum(e.count_words() for e in dev_corpus.exemplars) == 20
    assert dev_corpus.validate()


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
