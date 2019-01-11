#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text line cleaning functions. For WER calculations, final text should be utf chars a-z and \'
"""

from __future__ import print_function
import re
from collections import OrderedDict
import argparse
import num2words


def contains_digit(input_string):
  """
  check if string contains digit
  >>> contains_digit("5")
  True
  >>> contains_digit("5a")
  True
  >>> contains_digit("cat")
  False
  """
  return any(_.isdigit() for _ in input_string)


def ordinal_to_string(input_string):
  """
  convert strings '1st', '2nd', '3rd', ... to a string/word with chars a-z
  >>> ordinal_to_string("4th")
  'fourth'
  """

  def has_ordinal(input_string):
    " checks if input_string has ordinal "
    return contains_digit(input_string) and (
      input_string[-2:] == 'st' or input_string[-2:] == 'nd' or input_string[-2:] == 'rd' or input_string[-2:] == 'th'
    )

  ret_str = input_string

  if has_ordinal(input_string):
    ret_str = (num2words.num2words(int(input_string[:-2]), ordinal=True)).replace(',', '').replace('-', ' ')

  return ret_str


def dollars_to_string(input_string):
  """
  convert dollar strings '$2', '$2.56', '$10', '$1000000', ... to a string/word with chars a-z
  >>> dollars_to_string("$2.56")
  'two dollars and fifty six cents'
  >>> dollars_to_string("$3.")
  'three dollars'
  >>> dollars_to_string("$3.5")
  'three dollars and fifty cents'
  >>> dollars_to_string("$1")
  'one dollar'
  >>> dollars_to_string("$1.00")
  'one dollar and zero cents'
  >>> dollars_to_string("$1.01")
  'one dollar and one cent'
  """

  def format_dollars(dollar_string, dollars):
    " format dollar string "
    return dollar_string + " dollars" if dollars and int(dollars) != 1 else "one dollar"

  def format_cents(cents_string, cents):
    " format cent string "
    return (" and {:} cents".format(cents_string)
            if int(cents) != 1 else " and one cent") if (cents_string and cents) else ""

  input_string = input_string.replace("$", "")

  dollars, cents = input_string.split(".") if '.' in input_string else [input_string, None]

  dollar_words, cent_words = list(
    map(
      lambda num: num2words.num2words(int(num)) if num else None,
      [dollars, cents + "0" if (cents and len(cents) == 1) else cents]
    )
  )
  ret_str = format_dollars(dollar_words, dollars) + format_cents(cent_words, cents)

  return ret_str.replace("-", " ")


def digits_to_string(input_string):
  """
  convert strings '52.4' to string/word with chars a-z
  >>> digits_to_string("2.56")
  'two point fifty six'
  >>> digits_to_string("2")
  'two'
  >>> digits_to_string("1.05")
  'one point zero five'
  """

  def get_numbers_after_decicmal_point(input_string):
    " Catch everything after decimal point "
    ret_str = ""
    decimal = input_string.split(".")[1].strip() if len(input_string.split(".")) > 1 else ""
    if decimal:
      ret_str += " point"
      ret_str += " zero" * decimal.count("0")
      ret_str += " " + num2words.num2words(int(decimal))
    return ret_str

  ret_str = input_string
  if input_string:
    ret_str = num2words.num2words(int(input_string.split(".")[0])) if input_string.split(".")[0] != '' else ''
    ret_str += get_numbers_after_decicmal_point(input_string)

  return ret_str.replace("-", " ")


def pluralize(substring):
  """
  Convert number to number + plural ending
  >>> pluralize("5")
  'fives'
  >>> pluralize("6")
  'sixes'
  >>> pluralize("10")
  'tens'
  >>> pluralize("20")
  'twenties'
  """

  # default return value
  ret_str = substring

  def is_multiple_of_ten(notten):
    "check for twenties, etc. but not 1-10, 100, 1000, etc."
    return len(notten) == 2 and notten != "00" and notten != '10' and notten[-1] == '0'

  if is_multiple_of_ten(substring):
    ret_str = digits_to_string(substring)[:-1] + "ies"
  else:
    ret_str = digits_to_string(substring) + ('es' if substring[-1] == '6' else 's')
  return ret_str


def plural_numbers_to_string(input_string):
  """
  Converts plural numbers to strings
  >>> plural_numbers_to_string("6s")
  'sixes'
  >>> plural_numbers_to_string("8s")
  'eights'
  >>> plural_numbers_to_string("80s")
  'eighties'
  >>> plural_numbers_to_string("1980s")
  'nineteen eighties'
  """
  input_string = "".join(_ for _ in input_string if _.isdigit())

  ret_str = (
    " ".join((digits_to_string(input_string[:2]), pluralize(input_string[2:]))) if
    (len(input_string) == 4 and input_string[-2:] != "00") else pluralize(input_string)
  )

  return ret_str


def fraction_to_string(input_string):
  """
  Converts fraction to string
  >>> fraction_to_string("1/5")
  'one fifth'
  """

  numerator, denominator = input_string.split("/")

  # remove spaces
  numerator = numerator.strip()
  denominator = denominator.strip()

  numerator = digits_to_string(numerator)
  denominator = num2words.num2words(int(denominator), ordinal=True)
  return " ".join([numerator, denominator])


rematch = OrderedDict(
  [
    ("elipses", (re.compile(r"\.{2,}"), lambda m: " ")),
    ("websites", (re.compile(r"[.](net|org|com|gov)\b"), lambda m: " dot " + m.group().lower().replace(".", ""))),
    (
      "phone_numbers", (
        re.compile(r"\b((1|44)[ -.]?)?([\(]?([0-9]{1,}[\)]?[ -.]?){2,5})[0-9]{4}\b"),
        lambda m: " ".join(digits_to_string(_) for _ in m.group() if _.isdigit())
      )
    ),
    ("acronyms", (re.compile(r"\b(([A-Z]){1,}[.]?){2,}\b"), lambda m: " ".join(m.group().lower().replace(".", "")))),
    ("dashes", (re.compile(r"\-[0-9]\b"), lambda m: "negative " + m.group()[1:])),
    ("negatives", (re.compile(r" \- "), lambda m: "")),
    ("positives", (re.compile(r"\+"), lambda m: " plus ")),
    ("ordinals", (re.compile(r"[0-9]{1,}(st|nd|rd|th)"), lambda m: ordinal_to_string(m.group()))),
    (
      "many_dollars", (
        re.compile(r"\$([0-9]{1,}\.?[0-9]{0,})\s(billion|million|trillion)"),
        lambda m: " ".join([digits_to_string(m.groups()[0]), m.groups()[1], "dollars"])
      )
    ),
    ("dollars", (re.compile(r"\$[0-9]{1,}\.?[0-9]{0,}\w"), lambda m: dollars_to_string(m.group()))),
    ("percent", (re.compile(r"\%"), lambda m: " percent")),
    ("fractions", (re.compile(r"\b[0-9]\s?\/\s[0-9]\b"), lambda m: fraction_to_string(m.group()))),
    ("plural_numbers", (re.compile(r"\b[0-9]{1,}s\b"), lambda m: plural_numbers_to_string(m.group()))),
    ("numbers", (re.compile(r"[0-9\.]{1,}"), lambda m: " " + digits_to_string(m.group()) + " ")),
    ("apostrophes", (re.compile(r"\'"), lambda m: " \'")),
  ]
)


def clean_up(input_line):
  """
    Apply all text cleaning operations to input line
    >>> clean_up("his license plate is a. c, f seven...five ! zero")
    'his license plate is a c f seven five zero'
    >>> clean_up("Q2")
    'q two'
    >>> clean_up("from our website at www.take2games.com.")
    'from our website at www take two games dot com'
    >>> clean_up("NBA 2K18")
    'n b a two k eighteen'
    >>> clean_up("launched WWE 2K 18")
    'launched w w e two k eighteen'
    >>> clean_up("released L.A. Noire, the The VR Case Files for the HTC VIVE system")
    'released l a noire the the v r case files for the h t c v i v e system'
    >>> clean_up("Total net bookings were $654 million,")
    'total net bookings were six hundred and fifty four million dollars'
    >>> clean_up("net booking which grew 6% to $380 million.")
    'net booking which grew six percent to three hundred and eighty million dollars'
    >>> clean_up("to $25 dollars or $0.21 per share price.")
    'to twenty five dollars dollars or zero dollars and twenty one cents per share price'
    >>> clean_up("year-over-year")
    'year over year'
    >>> clean_up("HTC VIVE")
    'h t c v i v e'
    >>> clean_up("you can reach me at 1-(317)-222-2222 or fax me at 555-555-5555")
    'you can reach me at one three one seven two two two two two two two or fax me at five five five five five five five five five five'
  """
  for char_to_replace in ",*&!?":
    input_line = input_line.replace(char_to_replace, ' ')

  for pat in rematch:
    input_line = re.sub(rematch[pat][0], rematch[pat][1], input_line)

  for char_to_replace in ",.-":
    input_line = input_line.replace(char_to_replace, ' ')

  input_line = input_line.encode().decode('utf-8').lower()

  # check for double spacing
  while "  " in input_line:
    input_line = input_line.replace("  ", " ")
  return input_line.strip()


def clean_text_file(input_text_file):
  """
    Clean a text file
  """

  with open(input_text_file, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

  cleaned = []
  for line in lines:
    cleaned.append(clean_up(line))

  with open(input_text_file.replace('.txt', '') + '_cleaned.txt', 'w', encoding='utf-8') as f:
    f.write(" ".join(cleaned))

  print('File output: ' + input_text_file.replace('.txt', '') + '_cleaned.txt')


def main():
  """
    Either run tests or clean formatting for files, depending on # of arguments
  """

  parser = argparse.ArgumentParser(description='cleans input *.txt files and outputs *_cleaned.txt')
  parser.add_argument('files', type=str, nargs='+', help='list of input files')

  args = parser.parse_args()
  for file_name in args.files:
    extension = file_name.split(".")[-1]
    if extension != 'txt':
      print("File {:} does not end in .txt - please only use this for cleaning txt files".format(file_name))
      continue
    clean_text_file(file_name)


if __name__ == '__main__':
  main()
