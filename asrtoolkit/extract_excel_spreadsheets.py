#!/usr/bin/env python
"""
python extract_excel_spreadsheets foldername

Parses all spreadsheets in an input folder, extracts text,
and formats it into a target corpus folder for language model training
"""

import os
import pandas as pd
from asrtoolkit.clean_formatting import clean_up
from asrtoolkit.file_utils.name_cleaners import basename, strip_extension, sanitize
from glob import glob
import argparse


def extract_xlsx(filename, target_folder):
  """
  For an excel spreadsheet, extract to a text file
  """
  working_excel_data_structure = pd.ExcelFile(filename)
  raw_name = sanitize(strip_extension(basename(filename)))

  with open(''.join([target_folder, '/', raw_name, ".txt"]), 'a+') as f:
    for sheet in working_excel_data_structure.sheet_names:
      data = working_excel_data_structure.parse(sheet).values
      output_lines = "\n".join([" ".join([str(_) for _ in line if not pd.isnull(_)]) for line in data]).splitlines()
      f.write("\n".join((clean_up(line) for line in output_lines if line != "")))


def proc_input_dir_to_corpus(input_dir, output_dir):
  """
    Take an input dir of excel spreadsheets and process it to an output corpus dir of text files
  """
  os.makedirs(output_dir, exist_ok=True)

  for spreadsheet in glob(input_dir + "/*.xlsx") + glob(input_dir + "/*.xls"):
    extract_xlsx(spreadsheet, output_dir)


def main():
  parser = argparse.ArgumentParser(description='convert a folder of excel spreadsheets to a corpus of text files')
  parser.add_argument(
    '--input-folder', default='./', type=str, help='input folder of excel spreadsheets ending in .xls or .xlsx'
  )
  parser.add_argument('--output-corpus', default='corpus', type=str, help='output folder for storing text corpus')
  args = parser.parse_args()
  proc_input_dir_to_corpus(args.input_folder, args.output_corpus)


if __name__ == "__main__":
  main()
