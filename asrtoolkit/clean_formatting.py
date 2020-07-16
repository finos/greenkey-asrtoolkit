#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text line cleaning functions. For WER calculations, final text should be utf letter chars and \'
"""

import logging
import string
from collections import OrderedDict

import regex as re
from fire import Fire

from asrtoolkit.deformatting_utils import (
    digits_to_string,
    dollars_to_string,
    fraction_to_string,
    ordinal_to_string,
    plural_numbers_to_string,
)
from asrtoolkit.file_utils.script_input_validation import valid_input_file

LOGGER = logging.getLogger(__name__)

# preserve any unicode letters
invalid_chars = re.compile(r"[^\p{L}<\[\]> \']", re.IGNORECASE)

spaces = re.compile(r"\s+")

KNOWN_REPLACEMENTS = OrderedDict([
    ("millions", (re.compile(r"\b(mln|mio|mlns)\b"), lambda m: "million")),
    ("pleases", (re.compile(r"\b(plz|pls)\b"), lambda m: "please")),
    ("thanks", (re.compile(r"\b(thks|thx)\b"), lambda m: "thanks")),
    ("otc", (re.compile(r"\b(otc)\b"), lambda m: "o t c")),
    ("ellipses", (re.compile(r"\.{2,}"), lambda m: " ")),
    (
        "websites",
        (
            re.compile(r"[.](net|org|com|gov)\b"),
            lambda m: " dot " + m.group().lower().replace(".", ""),
        ),
    ),
    (
        "phone_numbers",
        (
            re.compile(
                r"\b((1|44)[ -.]?)?([\(]?([0-9]{1,}[\)]?[ -.]?){2,5})[0-9]{4}\b"
            ),
            lambda m: " ".join(
                digits_to_string(_) for _ in m.group() if _.isdigit()),
        ),
    ),
    (
        "acronyms",
        (
            re.compile(r"\b(([A-Z]){1,}[.]?){2,}\b"),
            lambda m: " ".join(m.group().lower().replace(".", "")),
        ),
    ),
    ("dashes", (re.compile(r"\-[0-9]\b"),
                lambda m: "negative " + m.group()[1:])),
    ("negatives", (re.compile(r" \- "), lambda m: "")),
    ("positives", (re.compile(r"\+"), lambda m: " plus ")),
    (
        "ordinals",
        (
            re.compile(r"[0-9]{1,}(st|nd|rd|th)"),
            lambda m: ordinal_to_string(m.group()),
        ),
    ),
    (
        "many_dollars",
        (
            re.compile(
                r"\$([0-9]{1,}\.?[0-9]{0,})\s(billion|million|trillion)"),
            lambda m: " ".join(
                [digits_to_string(m.groups()[0]),
                 m.groups()[1], "dollars"]),
        ),
    ),
    (
        "dollars",
        (
            re.compile(r"\$[0-9]{1,}\.?[0-9]{0,}[mbkMBK]?"),
            lambda m: dollars_to_string(m.group()),
        ),
    ),
    ("percent", (re.compile(r"\%"), lambda m: " percent")),
    (
        "fractions",
        (
            re.compile(r"\b[0-9]\s?\/\s?[0-9]\b"),
            lambda m: fraction_to_string(m.group()),
        ),
    ),
    (
        "plural_numbers",
        (
            re.compile(r"\b[0-9]{1,}s\b"),
            lambda m: plural_numbers_to_string(m.group()),
        ),
    ),
    (
        "numbers",
        (
            re.compile(r"[0-9\.]{1,}"),
            lambda m: " " + digits_to_string(m.group()) + " ",
        ),
    ),
    ("apostrophes", (re.compile(r"\'"), lambda m: " '")),
])


def remove_special_chars(line, chars_to_replace):
    "remove a set of special chars"
    for char_to_replace in chars_to_replace:
        line = line.replace(char_to_replace, " ")
    return line


def remove_all_special_chars(line):
    """
    Only allow unicode letter characters, spaces, apostrophes, 
    and angle brackets (for noises) to be output
    """
    return invalid_chars.sub(" ", line)


def remove_double_spaces(line):
    """
    Remove all double spaces
    """
    return spaces.sub(" ", line)


def apply_all_regex_and_replacements(input_line):
    """
    For a line and list of paired regex and replacements, 
      apply all replacements for all regex on the line
    """

    for pat in KNOWN_REPLACEMENTS:
        try:
            input_line = re.sub(KNOWN_REPLACEMENTS[pat][0],
                                KNOWN_REPLACEMENTS[pat][1], input_line)
        except Exception as exc:
            LOGGER.exception("Exception %s with line %s for pattern %s", exc,
                             input_line, pat)

    return input_line


def check_for_formatted_chars(input_line):
    "returns True if formatting or special chars are present otherwise False"

    return bool(set(input_line).difference(set(string.ascii_lowercase + " ")))


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
    >>> clean_up("I heard Mr. McDonald has $6.23")
    'i heard mr mcdonald has six dollars and twenty three cents'
    >>> clean_up(" for client X (hide name pls), plz giv $1 mln shs thx")
    'for client x hide name please please giv one million dollars shs thanks'
    >>> clean_up("[laughter]")
    '[laughter]'
    """

    if check_for_formatted_chars(input_line):

        input_line = remove_special_chars(input_line, ",*&!?")

        input_line = apply_all_regex_and_replacements(input_line)

        input_line = remove_all_special_chars(input_line)

        input_line = input_line.encode().decode("utf-8").lower()

    # check for double spacing
    input_line = remove_double_spaces(input_line)

    return input_line.strip()


def clean_one_file(input_text_file):
    """
    Cleans a single file
    """
    with open(input_text_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    cleaned = map(clean_up, lines)

    with open(input_text_file.replace(".txt", "") + "_cleaned.txt",
              "w",
              encoding="utf-8") as f:
        f.write(" ".join(cleaned))


def clean_text_file(*input_text_files):
    """
    Cleans input *.txt files and outputs *_cleaned.txt
    """
    for input_text_file in input_text_files:
        if not valid_input_file(input_text_file, valid_extensions=["txt"]):
            LOGGER.error(
                "File %s does not end in .txt - please only use this for cleaning txt files",
                input_text_file,
            )
            continue
        clean_one_file(input_text_file)

        LOGGER.info("File output: %s",
                    input_text_file.replace(".txt", "_cleaned.txt"))


def cli():
    Fire(clean_text_file)


if __name__ == "__main__":
    cli()
