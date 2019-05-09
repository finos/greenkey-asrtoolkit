#!/usr/bin/env python
"""
Python function for computing word error rates metric for Automatic Speech Recognition files
"""

import argparse
import editdistance
import re

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.clean_formatting import clean_up

# defines global regex for tagged noises and silence
re_tagged_nonspeech = re.compile(r"[\[<][A-Za-z #]*[\]>]")

# defines global regex to remove these nsns
nonsilence_noises = ["noise", "um", "ah", "er", "umm", "uh", "mm", "mn", "mhm", "mnh", "huh", "hmm"]
re_nonsilence_noises = re.compile(r"\b({})\b".format("|".join(nonsilence_noises)))


def remove_nonsilence_noises(input_text):
  """
    Removes nonsilence noises from a transcript
  """
  return re.sub(re_nonsilence_noises, '', input_text)


def wer(ref, hyp, remove_nsns=False):
  """
    Calculate word error rate between two string or time_aligned_text objects
    >>> wer("this is a cat", "this is a dog")
    25.0
  """

  # accept time_aligned_text objects too
  if type(ref) == time_aligned_text:
    ref = ref.text()

  if type(hyp) == time_aligned_text:
    hyp = hyp.text()

  # remove tagged noises and other nonspeech events
  ref = re.sub(re_tagged_nonspeech, ' ', ref)
  hyp = re.sub(re_tagged_nonspeech, ' ', hyp)

  # optionally, remove non silence noises
  if remove_nsns:
    ref = remove_nonsilence_noises(ref)
    hyp = remove_nonsilence_noises(hyp)

  # clean punctuation, etc.
  ref = clean_up(ref)
  hyp = clean_up(hyp)

  # calculate WER
  return 100 * editdistance.eval(ref.split(' '), hyp.split(' ')) / len(ref.split(' '))


def cer(ref, hyp, remove_nsns=False):
  """
    Calculate character error rate between two strings or time_aligned_text objects
    >>> cer("this cat", "this bad")
    25.0
  """

  # accept time_aligned_text objects too
  if type(ref) == time_aligned_text:
    ref = ref.text()

  if type(hyp) == time_aligned_text:
    hyp = hyp.text()

  if remove_nsns:
    ref = remove_nonsilence_noises(ref)
    hyp = remove_nonsilence_noises(hyp)

  ref = clean_up(ref)
  hyp = clean_up(hyp)

  # calculate per line CER
  return 100 * editdistance.eval(ref, hyp) / len(ref)


def main():
  parser = argparse.ArgumentParser(
    description='Compares a reference and transcript file and calculates word error rate (WER) between these two files'
  )
  parser.add_argument('reference_file', metavar='reference_file', type=str, help='reference "truth" file')
  parser.add_argument(
    'transcript_file', metavar='transcript_file', type=str, help='transcript possibly containing errors'
  )
  parser.add_argument(
    "--char-level", help="calculate character error rate instead of word error rate", action="store_true"
  )
  parser.add_argument("--ignore-nsns", help="ignore non silence noises like um, uh, etc.", action="store_true")

  # parse arguments
  args = parser.parse_args()

  # read files from arguments
  ref = time_aligned_text(args.reference_file)
  hyp = time_aligned_text(args.transcript_file)

  if args.char_level:
    print("CER: {:5.3f}%".format(cer(ref, hyp, args.ignore_nsns)))
  else:
    print("WER: {:5.3f}%".format(wer(ref, hyp, args.ignore_nsns)))


if __name__ == "__main__":
  main()
