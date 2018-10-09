#!/usr/bin/env python
"""
Python function for computing word error rates metric for Automatic Speech Recognition files
"""

import argparse
import difflib
import editdistance
import re

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.clean_formatting import clean_up


def wer(ref, hyp):
  """
    Calculate word error rate between two lists of strings
  """

  # calculate per line WER
  word_error_rate = [
    100 * editdistance.eval(ref_line.split(), hyp_line.split()) / len(ref_line.split())
    for ref_line, hyp_line in zip(ref, hyp)
  ]

  # average by weighting each line by # of words in references
  total_wer = sum([error_rate * len(ref_line.split()) for error_rate, ref_line in zip(word_error_rate, ref)]) \
                / sum(map(lambda l: len(l.split()), ref))

  return total_wer


def cer(ref, hyp):
  """
    Calculate character error rate between two lists of strings
  """

  # calculate per line CER
  char_error_rate = [
    100 * editdistance.eval(ref_line, hyp_line) / len(ref_line) for ref_line, hyp_line in zip(ref, hyp)
  ]

  # average by weighting each line by # of characters in reference
  total_cer = sum([error_rate * len(ref_line) for error_rate, ref_line in zip(char_error_rate, ref)]) \
                / sum(map(lambda l: len(l), ref))

  return total_cer


# defines global regex to remove these nsns
nonsilence_noises = ["noise", "um", "ah", "er", "umm", "uh"]
re_nonsilence_noises = re.compile(r"\b({})\b".format("|".join(nonsilence_noises)))


def remove_nonsilence_noises(input_text):
  """
    Removes nonsilence noises from a transcript
  """
  return re.sub(re_nonsilence_noises, '', input_text)


def main():
  parser = argparse.ArgumentParser(
    description='Compares a reference and transcript file and calculates word error rate (WER) between these two files'
  )
  parser.add_argument('reference_file', metavar='reference_file', type=str, help='reference "truth" file')
  parser.add_argument(
    'transcript_file', metavar='transcript_file', type=str, help='transcript possibly containing errors'
  )
  parser.add_argument("--diff", help="verbosely print differences", action="store_true")
  parser.add_argument(
    "--char-level", help="calculate character error rate instead of word error rate", action="store_true"
  )
  parser.add_argument("--ignore-nsns", help="ignore non silence noises like um, uh, etc.", action="store_true")

  # parse arguments
  args = parser.parse_args()

  # read files from arguments
  reference_file = time_aligned_text(args.reference_file)
  transcript_file = time_aligned_text(args.transcript_file)

  # note that we need to set the extensions to txt in order to get only txt back from the __str__ function
  reference_file.file_extension = 'txt'
  transcript_file.file_extension = 'txt'

  if args.diff:
    # optionally, do pretty printing of differences
    ref_text = clean_up(reference_file.__str__()).splitlines(keepends=True)
    hyp_text = clean_up(transcript_file.__str__()).splitlines(keepends=True)
    print("-" * 80)
    print("".join(difflib.ndiff(ref_text, hyp_text)), end="")
    print("\n" + "-" * 80)

  # apply clean up functions and split to a list of lines
  ref = clean_up(reference_file.__str__()).splitlines()
  hyp = clean_up(transcript_file.__str__()).splitlines()

  if args.ignore_nsns:
    # ignore non silence noises and remove them from a transcript
    ref = [remove_nonsilence_noises(line) for line in ref]
    hyp = [remove_nonsilence_noises(line) for line in hyp]

  if args.char_level:
    print("CER: {:5.3f}%".format(cer(ref, hyp)))
  else:
    print("WER: {:5.3f}%".format(wer(ref, hyp)))


if __name__ == "__main__":
  main()
