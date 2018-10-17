#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text line cleaning functions. For WER calculations, final text should be utf chars a-z and \'
"""

from __future__ import print_function
import re
import sys
from collections import OrderedDict
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


def contains_dollar_sign(input_string):
  """
    check if string contains '$'
  >>> contains_dollar_sign("$5")
  True
  >>> contains_dollar_sign("5")
  False
  """
  return any(_ == "$" for _ in input_string)


def dollars_to_string(input_string):
  """
  convert dollar strings '$2', '$2.56', '$10', '$1000000', ... to a string/word with chars a-z
  >>> dollars_to_string("$2.56")
  'two dollars and fifty six cents'
  >>> dollars_to_string("$3.")
  'three dollars'
  >>> dollars_to_string("$3.5")
  'three dollars and fifty cents'
  """
  ret_str = input_string
  if contains_dollar_sign(input_string):
    input_string = input_string.replace("$", "")
    dollars, cents = input_string.split(".")
    if len(cents) == 1:
      cents += "0"
    ret_str = " dollars and ".join(
      num2words.num2words(int(number)) if all(c.isdigit()
                                              for c in number) else number
      for number in [dollars, cents]
      if number
    )
    ret_str += (
      " cents" if '.' in input_string and len([_ for _ in input_string.split(".") if _]) > 1 else
      (" dollars" if '.' in input_string else "")
    )

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
  ret_str = input_string
  if input_string:
    ret_str = num2words.num2words(int(input_string.split(".")[0])) if input_string.split(".")[0] != '' else ''
    if len(input_string.split(".")) > 1:
      decimal = input_string.split(".")[1].strip()
      if decimal:
        ret_str += " point"
        ret_str += " zero" * decimal.count("0")
        ret_str += " " + num2words.num2words(int(decimal))

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
  """
  # inline lambda to pluralize decades/tens

  input_string = "".join(_ for _ in input_string if _.isdigit())
  ret_str = input_string

  if len(input_string) == 4 and input_string[-2:] != "00":
    part1 = digits_to_string(int(input_string[:2]))
    part2 = pluralize(input_string[2:])
    ret_str = " ".join((part1, part2))
  elif input_string:
    ret_str = pluralize(input_string)

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
      "acronyms",
      (re.compile(r"\b[A-Z][.]?[A-Z][.]?[A-Z][.]?\b"), lambda m: " ".join(m.group().lower().replace(".", "")))
    ),
    ("dashes", (re.compile(r"\-[0-9]\b"), lambda m: "negative " + m.group()[1:])),
    ("negatives", (re.compile(r" \- "), lambda m: "")),
    ("positives", (re.compile(r"\+"), lambda m: " plus ")),
    ("ordinals", (re.compile(r"[0-9]{1,}(st|nd|rd|th)"), lambda m: ordinal_to_string(m.group()))),
    (
      "many_dollars", (
        re.compile(r"\$([0-9]{1,}\.?[0-9]{0,})\s(billion|million|trillion)"),
        lambda m: " ".join([dollars_to_string(m.groups()[0]), m.groups()[1], "dollars"])
      )
    ),
    ("dollars", (re.compile(r"\$[0-9]{1,}\.?[0-9]{0,}\w"), lambda m: dollars_to_string(m.group()))),
    ("percent", (re.compile(r"\%"), lambda m: " percent")),
    ("fractions", (re.compile(r"\b[0-9]\s?\/\s[0-9]\b"), lambda m: fraction_to_string(m.group()))),
    ("plural_numbers", (re.compile(r"\b[0-9]{1,}s\b"), lambda m: plural_numbers_to_string(m.group()))),
    ("numbers", (re.compile(r"[0-9\.]{1,}"), lambda m: digits_to_string(m.group()))),
    ("apostrophes", (re.compile(r"\'"), lambda m: " \'")),
  ]
)


def clean_up(input_line):
  """
    Apply all text cleaning operations to input line
    >>> clean_up("his license plate is a. c, f seven...five ! zero")
    'his license plate is a c f seven five zero'
  """
  for char_to_replace in [',', '*', '&', '!', '?']:
    input_line = input_line.replace(char_to_replace, '')

  for pat in rematch:
    input_line = re.sub(rematch[pat][0], rematch[pat][1], input_line)

  for char_to_replace in [',', '.', '-']:
    input_line = input_line.replace(char_to_replace, '')

  input_line = input_line.encode().decode('utf-8').lower()

  # check for double spacing
  while "  " in input_line:
    input_line = input_line.replace("  ", " ")
  return input_line.strip()


def main():
  """
    Either run tests or clean formatting for files, depending on # of arguments
  """
  if len(sys.argv) == 1:
    import doctest
    doctest.testmod()

  for file_name in sys.argv[1:]:
    extension = file_name.split(".")[-1]
    if extension != 'txt':
      print("File does not end in .txt - please only use this for cleaning txt files")
      continue

    with open(file_name, 'r', encoding='utf-8') as f:
      lines = f.readlines()

    cleaned = []
    for line in lines:
      cleaned.append(clean_up(line))

    with open(file_name.replace('.txt', '') + '_cleaned.txt', 'w', encoding='utf-8') as f:
      f.writelines(cleaned)

    print('File output: ' + file_name.replace('.txt', '') + '_cleaned.txt')


if __name__ == '__main__':
  main()
