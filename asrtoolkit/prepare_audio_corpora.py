#!/usr/bin/env python
"""
Script for preparing SPH, STM files into training, testing, and development sets from a set of corpora directories

If present, train, test, dev sets will be used from the individual corpora
"""

import os
import argparse

data_dirs = ["test", "train", "dev"]

from asrtoolkit.data_structures.corpus import corpus


def main():
  parser = argparse.ArgumentParser(
    description="Copy and organize specified corpora into a target directory. "
    "Training, testing, and development sets will be created automatically if not already defined."
  )
  parser.add_argument('--target-dir', default='input-data', required=False, help="Path to target directory")
  parser.add_argument('corpora', nargs='+', help="Name of one or more directories in directory this script is run")

  args = parser.parse_args()

  for data_dir in data_dirs:
    os.makedirs(args.target_dir + "/" + data_dir, exist_ok=True)

  corpora = {"dev": corpus(), "test": corpus(), "train": corpus(), "unsorted": corpus()}

  for corpus_dir in args.corpora:
    for data_dir in data_dirs:
      if os.path.exists(corpus_dir + "/" + data_dir):
        corpora[data_dir] += corpus({"location": corpus_dir + "/" + data_dir})
    corpora['unsorted'] += corpus({"location": corpus_dir})

  all_ready = all(corpora[data_dir].validate() for data_dir in data_dirs)
  # dump extra data into training data by default
  corpora['train'] += corpora['unsorted']
  if not all_ready:
    print("Not all training corpora were prepared. Automatically shuffling into training, testing, development sets")

    # first pass, populate train directory
    if not corpora['train'].validate():
      corpora['train'] += corpora['dev'] + corpora['test']

    # pick a file from training set to be dev set
    if not corpora['dev'].validate():
      corpora['dev'] = corpora['train'][-1]
      corpora['train'] = corpora['train'][:-1]

    # pick 20% for testing
    if not corpora['test'].validate():
      split_index = int(corpora['train'].validate() * 4 // 5)
      corpora['test'] = corpora['train'][split_index:]
      corpora['train'] = corpora['train'][:split_index]

  # prepare for training
  for data_dir in data_dirs:
    corpora[data_dir].prepare_for_training(args.target_dir + "/" + data_dir)


if __name__ == "__main__":
  main()
