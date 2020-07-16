#!/usr/bin/env python
"""
Script for preparing SPH, STM files into training, testing, and development sets from a set of corpora directories

If present, train, test, dev sets will be used from the individual corpora
"""
import json
import logging

from fire import Fire

from asrtoolkit.data_structures.corpus import corpus
from asrtoolkit.file_utils.common_file_operations import make_list_of_dirs

LOGGER = logging.getLogger()

data_dirs = ["test", "train", "dev"]


def auto_split_corpora(corpora, min_size=50):
    """
    Given input corpora dict of corpora, auto split if it isn't already split
    """
    all_ready = all(
        corpora[data_dir].validate() if data_dir in corpora else False
        for data_dir in data_dirs)

    # dump extra data into training data by default
    if "unsorted" in corpora:
        corpora["train"] += corpora["unsorted"]
    if not all_ready:
        LOGGER.warning(
            "Not all training corpora were prepared. Automatically shuffling into training, testing, development sets"
        )

        # first pass, populate train directory
        corpora["train"] += corpora["dev"] + corpora["test"]

        # pick a file from training set to be dev set such that it contains min_size segments
        corpora["dev"], corpora["train"] = corpora["train"][:1], corpora[
            "train"][1:]
        while (corpora["dev"].calculate_number_of_segments() < min_size
               and corpora["train"].validate() > 0):
            corpora["dev"], corpora["train"] = (
                (corpora["dev"] + corpora["train"][:1]),
                corpora["train"][1:],
            )

        # pick 20% for testing
        split_index = len(corpora["train"].exemplars) * 4 // 5
        corpora["test"] = corpora["train"][split_index:]
        corpora["train"] = corpora["train"][:split_index]

        # ensure no duplicates
        corpora["train"] -= corpora["test"]
        corpora["test"] -= corpora["dev"]
        corpora["train"] -= corpora["dev"]

    if (corpora["dev"].calculate_number_of_segments() < min_size
            or corpora["train"].calculate_number_of_segments() < min_size):

        # throw error
        raise (Exception(
            "Error - insufficient data - please add more and try again"))

    else:
        return corpora


def get_corpus(loc):
    """ returns corpus for input location """
    return corpus({"location": loc})


def prep_all_for_training(corpora, target_dir, nested, sample_rate=16000):
    """
    prepare all corpora for training and return logs of what was where
    """
    return {
        data_dir:
        corpora[data_dir].prepare_for_training(target_dir + "/" + data_dir,
                                               nested, sample_rate)
        for data_dir in data_dirs
    }


def gather_all_corpora(corpora_dirs):
    """
    Finds all existing corpora and gathers into a dictionary
    """

    corpora = {
        data_dir: get_corpus(corpus_dir + "/" + data_dir)
        for corpus_dir in corpora_dirs for data_dir in data_dirs
    }

    corpora["unsorted"] = corpus()
    for unsorted_corpus in list(map(get_corpus, corpora_dirs)):
        corpora["unsorted"] += unsorted_corpus
    return corpora


def prepare_audio_corpora(*corpora, target_dir="input-data", nested=False):
    """
    Copy and organize specified corpora into a target directory.
    Training, testing, and development sets will be created automatically if not already defined.

    Input
        corpora, strs - name of one or more directories to combine into `target-dir`
        target-dir, str - target directory where corpora should be organized
        nested, bool (default False)- if present/True, store in stm and sph subdirectories
    """

    make_list_of_dirs([
        target_dir + "/" + data_dir + subdirectory for data_dir in data_dirs
        for subdirectory in (["/stm/", "/sph/"] if nested else ["/"])
    ])

    corpora = gather_all_corpora(corpora)
    corpora = auto_split_corpora(corpora)

    log = prep_all_for_training(corpora, target_dir, nested)
    with open(target_dir + "/corpora.json", "w") as f:
        f.write(json.dumps(log))


def cli():
    Fire(prepare_audio_corpora)


if __name__ == "__main__":
    cli()
