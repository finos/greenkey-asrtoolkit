#!/usr/bin/env python
"""
Simple wrapper for name-cleaning functions
"""


def basename(file_name):
  """
    Returns basename of a file without the preceding directory
  """
  return file_name.split("/")[-1]


def strip_extension(file_name):
  """
    Returns file without extension
  """
  return ".".join(file_name.split(".")[:-1]) if file_name else ""


def sanitize(file_name, chars_to_replace='- ', silent=True):
  """
    replace input characters with underscores if present in file name
  >>> sanitize("-asdflkj_ .tmp")
  '_asdflkj__.tmp'
  """

  def replace_char(input_char, file_name):
    " replace specific char if present "
    if input_char in file_name and not silent:
      print(
        "replacing '{:}'s with underscores in sph file output - ".format(c) +
        "check to make sure your audio files and transcript files match"
      )
    return "/".join(file_name.split("/")[:-1] + [basename(file_name).replace(c, "_")])

  for c in chars_to_replace:
    file_name = replace_char(c, file_name)

  return file_name


def sanitize_hyphens(file_name, silent=True):
  """
    replace hyphens with underscores if present in file name
  """
  return sanitize(file_name, '-', silent=silent)


def generate_segmented_file_name(target_dir, file_name, iseg):
  """
    Take a target location, a current location, and a segment number and generate a target filename
  """
  return target_dir + "/" + basename(strip_extension(file_name)) + \
            "_seg_{:05d}.".format(iseg) + file_name.split(".")[-1]
