#!/usr/bin/env python
"""
Class for holding time_aligned text

"""

import os
import importlib
import hashlib
from asrtoolkit.file_utils.name_cleaners import sanitize_hyphens, generate_segmented_file_name


class time_aligned_text(object):
  """
  Class for storing time-aligned text and converting between formats
  """

  def __init__(self, input_data=None):
    """
    Instantiates a time_aligned text object from a file (if input_var is a string)

    >>> transcript = time_aligned_text()
    """
    self.location = ""
    self.segments = []
    self.file_extension = None

    if input_data is not None and isinstance(input_data, str) and os.path.exists(input_data):
      self.read(input_data)
    elif input_data is not None and type(input_data) in [str, dict]:
      self.file_extension = 'txt' if isinstance(input_data, str) else 'json'
      data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format(self.file_extension))
      self.segments = data_handler.read_in_memory(input_data)

  def hash(self):
    """
      Returns a sha1 hash of the file
    """
    if self.location:
      with open(self.location) as f:
        return hashlib.sha1(f.read().encode()).hexdigest()
    else:
      return hashlib.sha1("".encode()).hexdigest()

  def __str__(self):
    """
      Returns string representation of formatted segments as corresponding
      By default, use the extension of the file you loaded
    >>> transcript = time_aligned_text()
    >>> print(transcript.__str__()=="")
    True
    """
    data_handler = importlib.import_module(
      "asrtoolkit.data_handlers.{:}".format(self.file_extension if self.file_extension else 'txt')
    )
    return "\n".join(_.__str__(data_handler) for _ in self.segments)

  def text(self):
    """
      Returns unformatted text from all segments
    """
    data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format('txt'))
    return " ".join(_.__str__(data_handler) for _ in self.segments)

  def read(self, file_name):
    """ Read a file using class-specific read function """
    self.file_extension = file_name.split(".")[-1]
    self.location = file_name
    data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format(self.file_extension))
    self.segments = data_handler.read_file(file_name)

  def write(self, file_name):
    """ Output to file using segment-specific __str__ function """
    file_extension = file_name.split(".")[-1] if '.' in file_name else 'stm'

    file_name = sanitize_hyphens(file_name)

    data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format(file_extension))
    with open(file_name, 'w', encoding="utf-8") as f:
      f.write(data_handler.header())
      f.writelines(data_handler.separator.join(seg.__str__(data_handler) for seg in self.segments))
      f.write(data_handler.footer())

    # return back new object in case we are updating a list in place
    return time_aligned_text(file_name)

  def split(self, target_dir):
    """
      Split transcript into many pieces based on valid segments of transcript
    """
    os.makedirs(target_dir, exist_ok=True)
    for iseg, seg in enumerate(self.segments):
      new_seg = time_aligned_text()
      new_seg.file_extension = self.file_extension
      new_seg.location = generate_segmented_file_name(target_dir, self.location, iseg)
      new_seg.segments = [seg]
      new_seg.write(new_seg.location)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
