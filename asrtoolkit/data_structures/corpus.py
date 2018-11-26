#!/usr/bin/env python
"""
Module for organizing SPH, STM files from a corpus
"""

import os
import glob
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm

from asrtoolkit.data_structures.audio_file import audio_file
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.file_utils.name_cleaners import basename, strip_extension


def get_files(data_dir, extension):
  """
    Gets all files in a data directory with given extension
  """
  files = []
  if data_dir and os.path.exists(data_dir):
    files = glob.glob(data_dir + "/*." + extension)
  return files


class exemplar(object):
  """
    Create an exemplar class to pair one audio file with one transcript file
  """

  def __init__(self, input_dict=None):
    self.audio_file = None
    self.transcript_file = None
    self.__dict__.update(input_dict if input_dict else {})

  def validate(self):
    " validate exemplar object by constraining that the filenames before the extension are the same "

    valid = True
    audio_filename = basename(strip_extension(self.audio_file.location))
    transcript_filename = basename(strip_extension(self.transcript_file.location))
    if audio_filename != transcript_filename:
      print(
        "Mismatch between audio and transcript filename - please check the following: \n" +
        ", ".join((audio_filename, transcript_filename))
      )
      valid = False

    if not os.path.getsize(self.audio_file.location):
      print("Audio file {:} is empty".format(self.audio_file.location))
      valid = False

    if not os.path.getsize(self.transcript_file.location):
      print("Transcript file {:} is empty".format(self.transcript_file.location))
      valid = False

    return valid

  def hash(self):
    """
      Returns combined hash of two files
    """
    return self.audio_file.hash() + self.transcript_file.hash()


class corpus(object):
  """
    Create a corpus object for storing information about where files are and how many
  """

  def __init__(self, input_dict=None):
    """
      Initialize from location and populate list of SPH, WAV, or MP3 audio files and STM files into segments
    """
    self.location = None
    self.exemplars = []
    self.__dict__.update(input_dict if input_dict else {})

    # only if not defined above should we search for exemplars based on location
    if not self.exemplars:
      audio_extensions_to_try = ["sph", "wav", "mp3"][::-1]
      self.exemplars += [
        exemplar({
          'audio_file': audio_file(fl),
          'transcript_file': time_aligned_text(strip_extension(fl) + ".stm")
        })
        for audio_extension in audio_extensions_to_try
        for fl in (get_files(self.location, audio_extension) if self.location else [])
        if (os.path.exists(strip_extension(fl) + ".stm"))
      ]

      # gather all exemplars from /stm and /sph subdirectories if present
      self.exemplars += [
        exemplar(
          {
            'audio_file': audio_file(fl),
            'transcript_file': time_aligned_text(self.location + "/stm/" + basename(strip_extension(fl)) + ".stm")
          }
        )
        for audio_extension in audio_extensions_to_try
        for fl in (get_files(self.location + "/sph/", audio_extension) if self.location else [])
        if (os.path.exists(self.location + "/stm/" + basename(strip_extension(fl)) + ".stm"))
      ]

  def validate(self):
    """
      Check to and validate each example after sorting by audio file hash since stm hash may change
    """
    dict_of_examples = {_.audio_file.hash(): _ for _ in self.exemplars}
    self.exemplars = [dict_of_examples[_] for _ in set(dict_of_examples)]
    return sum(_.validate() for _ in self.exemplars)

  def log(self):
    """
      Log what each hashed example contains
    """
    return {
      _.hash(): {
        'audio_file': _.audio_file.location,
        'audio_file_hash': _.audio_file.hash(),
        'transcript_file': _.transcript_file.location,
        'transcript_file_hash': _.transcript_file.hash()
      }
      for _ in self.exemplars
    }

  def prepare_for_training(self, target=None, nested=False):
    """
      Run validation and audio file preparation steps
    """

    # write corpus back in place if no target
    target = self.location if target is None else target

    executor = ThreadPoolExecutor()

    # process audio files concurrently for speed
    futures = [
      executor.submit(
        partial(
          _.audio_file.prepare_for_training, target + ("/sph/" if nested else "/") + basename(_.audio_file.location)
        )
      ) for _ in self.exemplars
    ]

    # trigger conversion and gather results
    audio_files = [future.result() for future in tqdm(futures)]

    transcript_files = [
      _.transcript_file.write(target + ("/stm/" if nested else "/") + basename(_.transcript_file.location))
      for _ in self.exemplars
    ]

    new_corpus = corpus(
      {
        "location":
          target,
        "exemplars":
          [exemplar({
            "audio_file": af,
            "transcript_file": tf
          }) for af, tf in zip(audio_files, transcript_files)],
      }
    )
    new_corpus.validate()
    return new_corpus.log()

  def __add__(self, other):
    """ Allow addition of corpora via + operator """
    return corpus({"location": None, "exemplars": self.exemplars + other.exemplars})

  def __iadd__(self, other):
    """ Allow addition of corpora via += operator """
    self.exemplars = self.exemplars + other.exemplars
    return self

  def __sub__(self, other):
    """ Allow addition of corpora via - operator """
    return corpus({"location": None, "exemplars": [_ for _ in self.exemplars if _ not in other.exemplars]})

  def __isub__(self, other):
    """ Allow subtraction of corpora via -= operator """
    self.exemplars = [_ for _ in self.exemplars if _ not in other.exemplars]
    return self

  def __getitem__(self, given):
    """ Allow slicing of corpora via [] """
    return corpus(
      {
        "location": self.location,
        "exemplars": [self.exemplars[given]] if not isinstance(given, slice) else self.exemplars[given]
      }
    )
