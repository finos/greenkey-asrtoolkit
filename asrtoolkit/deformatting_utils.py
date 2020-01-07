#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
De-Formatting functions used in clean_formatting
"""

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
        return contains_digit(input_string) and (input_string[-2:] == "st"
                                                 or input_string[-2:] == "nd"
                                                 or input_string[-2:] == "rd"
                                                 or input_string[-2:] == "th")

    ret_str = input_string

    if has_ordinal(input_string):
        ret_str = ((num2words.num2words(int(input_string[:-2]),
                                        ordinal=True)).replace(",",
                                                               "").replace(
                                                                   "-", " "))

    return ret_str


def format_dollars(dollar_string, dollars):
    " format dollar string "
    return dollar_string + " dollars" if dollars and int(
        dollars) != 1 else "one dollar"


def format_cents(cents_string, cents):
    " format cent string "
    return ((" and {:} cents".format(cents_string) if int(cents) != 1 else
             " and one cent") if (cents_string and cents) else "")


def format_quantities(input_string):
    " split off quantities and change into words"

    possible_quant = input_string[-1].upper() if input_string else ""
    quantity_dict = {"B": "billion", "M": "million", "K": "thousand"}
    quant = quantity_dict[
        possible_quant] if possible_quant in quantity_dict else ""

    if quant:
        input_string = input_string[:-1]

    return input_string, quant


def format_dollars_and_cents(input_string):
    "formats de-formatted dollars and cents from dollars and cents string"
    # split into pieces
    dollars, cents = (input_string.split(".")
                      if "." in input_string else [input_string, None])

    # format all as numbers
    dollar_words, cent_words = list(
        map(
            lambda num: num2words.num2words(int(num)) if num else None,
            [dollars, cents + "0" if (cents and len(cents) == 1) else cents],
        ))

    # format the output
    return format_dollars(dollar_words, dollars) + format_cents(
        cent_words, cents)


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
    >>> dollars_to_string("$1.01B")
    'one point zero one billion dollars'
    """

    input_string = input_string.replace("$", "")

    # peel off quantity if present
    input_string, quant = format_quantities(input_string)

    if not quant:
        ret_str = format_dollars_and_cents(input_string)
    else:
        ret_str = " ".join(
            [num2words.num2words(float(input_string)), quant, "dollars"])

    # remove minus signs
    ret_str = ret_str.replace("-", " ")

    return ret_str


def get_numbers_after_decicmal_point(input_string):
    " Format every number after decimal point "
    ret_str = ""
    decimal = (input_string.split(".")[1].strip()
               if len(input_string.split(".")) > 1 else "")
    if decimal:
        ret_str += " point"
        ret_str += " zero" * decimal.count("0")
        ret_str += " " + num2words.num2words(int(decimal))
    return ret_str


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
        ret_str = (num2words.num2words(int(input_string.split(".")[0]))
                   if input_string.split(".")[0] != "" else "")
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
        return (len(notten) == 2 and notten != "00" and notten != "10"
                and notten[-1] == "0")

    if is_multiple_of_ten(substring):
        ret_str = digits_to_string(substring)[:-1] + "ies"
    else:
        ret_str = digits_to_string(substring) + ("es" if substring[-1] == "6"
                                                 else "s")
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

    ret_str = (" ".join(
        (digits_to_string(input_string[:2]), pluralize(input_string[2:]))) if
               (len(input_string) == 4
                and input_string[-2:] != "00") else pluralize(input_string))

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
