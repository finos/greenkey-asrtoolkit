#!/usr/bin/env python
"""
Script for preparing SPH, STM files into training, testing, and development sets from a set of corpora directories

If present, train, test, dev sets will be used from the individual corpora
"""
import argparse
import json
data_dirs = ["test", "train", "dev"]

from asrtoolkit.data_structures.corpus import corpus
from asrtoolkit.file_utils.common_file_operations import make_list_of_dirs


def auto_split_corpora(corpora):
  """ given input corpora dict of corpora, auto split if it doesn't satisfy all_ready constraint """
  all_ready = all(corpora[data_dir].validate() if data_dir in corpora else False for data_dir in data_dirs)

  # dump extra data into training data by default
  corpora['train'] += corpora['unsorted']
  if not all_ready:
    print("Not all training corpora were prepared. Automatically shuffling into training, testing, development sets")

    # first pass, populate train directory
    corpora['train'] += corpora['dev'] + corpora['test']

    # pick a file from training set to be dev set
    corpora['dev'] = corpora['train'][-1]
    corpora['train'] = corpora['train'][:-1]

    # pick 20% for testing
    split_index = int(corpora['train'].validate() * 4 // 5)
    corpora['test'] = corpora['train'][split_index:]
    corpora['train'] = corpora['train'][:split_index]

    # ensure no duplicates
    corpora['train'] -= corpora['test']
    corpora['test'] -= corpora['dev']
    corpora['train'] -= corpora['dev']
  return corpora


def get_corpus(loc):
  """ returns corpus for input location """
  return corpus({"location": loc})


def prep_all_for_training(corpora, target_dir, nested):
  """
    prepare all corpora for training and return logs of what was where
  """
  return {
    data_dir: corpora[data_dir].prepare_for_training(target_dir + "/" + data_dir, nested) for data_dir in data_dirs
  }


def gather_all_corpora(corpora_dirs):
  """
    Finds all existing corpora and gathers into a dictionary
  """

  corpora = {data_dir: get_corpus(corpus_dir + "/" + data_dir) for corpus_dir in corpora_dirs for data_dir in data_dirs}

  corpora['unsorted'] = corpus()
  for unsorted_corpus in list(map(get_corpus, corpora_dirs)):
    corpora['unsorted'] += unsorted_corpus
  return corpora


def main():
  parser = argparse.ArgumentParser(
    description="Copy and organize specified corpora into a target directory. "
    "Training, testing, and development sets will be created automatically if not already defined."
  )
  parser.add_argument('--target-dir', default='input-data', required=False, help="Path to target directory")
  parser.add_argument(
    '--nested',
    action='store_true',
    default=False,
    required=False,
    help="if present, store output in stm and sph subdirectories"
  )
  parser.add_argument('corpora', nargs='+', help="Name of one or more directories in directory this script is run")

  args = parser.parse_args()

  make_list_of_dirs(
    [
      args.target_dir + "/" + data_dir + subdirectory
      for data_dir in data_dirs
      for subdirectory in (['/stm/', '/sph/'] if args.nested else ['/'])
    ]
  )

  corpora = gather_all_corpora(args.corpora)

  corpora = auto_split_corpora(corpora)

  log = prep_all_for_training(corpora, args.target_dir, args.nested)
  with open(args.target_dir + "/corpora.json", 'w') as f:
    f.write(json.dumps(log))


if __name__ == "__main__":
  main()
