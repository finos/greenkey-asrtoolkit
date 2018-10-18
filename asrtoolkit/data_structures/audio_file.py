#!/usr/bin/env python
"""
Module for holding information about an audio file and doing basic conversions
"""

import os
import subprocess
from asrtoolkit.file_utils.name_cleaners import sanitize_hyphens, generate_segmented_file_name, strip_extension


def cut_utterance(source_audio_file, target_audio_file, start_time, end_time, sample_rate=16000):
  """
    source_audio_file: str, path to file
    target_audio_file: str, path to file
    start_time: float or str
    end_time: float or str
    sample_rate: int, default 16000; audio sample rate in Hz

    uses sox segment source_audio_file to create target_audio_file that contains audio from start_time to end_time
        with audio sample rate set to sample_rate
    """
  subprocess.call(
    [
      "sox {} -r {} -b 16 -c 1 {} trim {} ={}"
      .format(source_audio_file, str(sample_rate), target_audio_file, str(start_time), str(end_time))
    ],
    shell=True
  )


def degrade_audio(source_audio_file, target_audio_file=None):
  """
    Degrades audio to typical G711 level. Useful if models need to target this audio quality.
  """

  target_audio_file = source_audio_file if target_audio_file is None else target_audio_file

  # degrade to 8k
  tmp1 = ".".join(source_audio_file.split(".")[:-1]) + "_tmp1.wav"
  subprocess.call(["sox {} -r 8000 -e a-law {}".format(source_audio_file, tmp1)], shell=True)

  # convert to u-law
  tmp2 = ".".join(source_audio_file.split(".")[:-1]) + "_tmp2.wav"
  subprocess.call(["sox {} --rate 8000 -e u-law {}".format(tmp1, tmp2)], shell=True)

  # upgrade to 16k a-law signed
  subprocess.call(["sox {} --rate 16000 -e signed  -b 16 --channel 1 {}".format(tmp2, target_audio_file)], shell=True)
  os.remove(tmp1)
  os.remove(tmp2)


class audio_file(object):
  """
    Create a corpus object for storing information about where files are and how many
  """
  location = None

  def __init__(self, location=""):
    """
    Populate file location into
    """
    if not os.path.exists(location):
      raise "File not found"
    self.location = location

  def prepare_for_training(self, file_name):
    """
      Converts to single channel (from channel 1) 16k audio file in SPH file format
    """
    if file_name.split(".")[-1] != 'sph':
      print("Forcing training data to use SPH file format")
      file_name = strip_extension(file_name) + ".sph"

    file_name = sanitize_hyphens(file_name)
    subprocess.call(["sox {} {} rate 16k remix -".format(self.location, file_name)], shell=True)

    # return new object
    return audio_file(file_name)

  def split(self, transcript, target_dir):
    """
      Split audio file and transcript into many pieces based on valid segments of transcript
    """

    os.makedirs(target_dir, exist_ok=True)
    for iseg, seg in enumerate(transcript.segments):
      cut_utterance(self.location, generate_segmented_file_name(target_dir, self.location, iseg), seg.start, seg.stop)
    transcript.split(target_dir)

    return
