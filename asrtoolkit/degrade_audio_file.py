#!/usr/bin/env python
"""
Script for degrading audio files to G711 audio quality
"""

import sys
from asrtoolkit.data_structures.audio_file import degrade_audio


def main():
  """
    Degrade all audio files given as arguments (in place by default)
  """
  for file_name in sys.argv[1:]:
    degrade_audio(file_name)


if __name__ == "__main__":
  main()
