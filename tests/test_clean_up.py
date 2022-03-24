#!/usr/bin/env python
"""
Test wer calculation
"""

from asrtoolkit.clean_formatting import clean_up


def test_clean_up():
    "execute suite of tests"

    tests = [
        ("1.05", "one point zero five"),
        ("105.", "one hundred and five"),
        ("105.", "one hundred and five"),
        ("They dollars and three cents.", "they dollars and three cents"),
        (
            "The machine is in the garden of Mr. MacGregor.",
            "the machine is in the garden of mr macgregor",
        ),
        ("This may be a problem.", "this may be a problem"),
        (
            "Yeah th those are my finest percentages.",
            "yeah th those are my finest percentages",
        ),
        ("Please press five after the tone.", "please press five after the tone"),
        ("Six distinct.", "six distinct"),
        ("ABC trades at -3.2%.", "a b c trades at negative three point two percent"),
        (
            "My 2017 report shows the 5th best earnings.",
            "my two thousand and seventeen report shows the fifth best earnings",
        ),
        ("This is the 9th of November.", "this is the ninth of november"),
        (
            "No work has been completed since Tuesday the 16th of September.",
            "no work has been completed since tuesday the sixteenth of september",
        ),
        (
            "That is what Leah Bradley said last week about the Indians on TV.",
            "that is what leah bradley said last week about the indians on t v",
        ),
        (
            "I've never done anything that I'd regret.",
            "i 've never done anything that i 'd regret",
        ),
        (
            "He needs 1.375%.",
            "he needs one point three hundred and seventy five percent",
        ),
        (
            "I heard Mr. McDonald has $6.23",
            "i heard mr mcdonald has six dollars and twenty three cents",
        ),
        ("Yes this is Mr. MacAllen.", "yes this is mr macallen"),
        ("Don't break dollars.", "don 't break dollars"),
        ("This is the best one.", "this is the best one"),
        ("London has five theatres.", "london has five theatres"),
        ("Hundreds of cats.", "hundreds of cats"),
        ("Thousands of cats.", "thousands of cats"),
        ("Millions and billions of cats.", "millions and billions of cats"),
        ("Good evening Larry.", "good evening larry"),
        ("You have two choices Neo.", "you have two choices neo"),
        ("This one or that one.", "this one or that one"),
        ("7 8 9 ...", "seven eight nine"),
        ("Two partridges in one pear tree.", "two partridges in one pear tree"),
        ("2s 3s 4s.", "twos threes fours"),
        ("I am -5 on the bonds.", "i am negative five on the bonds"),
        ("This is your bus terminus seven.", "this is your bus terminus seven"),
        ("5th of March.", "fifth of march"),
        ("Hundreds.", "hundreds"),
        ("ABC.", "a b c"),
        ("A.B.C.", "a b c"),
        ("ABC", "a b c"),
        ("A one sauce.", "a one sauce"),
        ("This is Prof. Charles Xavier.", "this is prof charles xavier"),
        ("Welcome to the island of Dr. Moreau.", "welcome to the island of dr moreau"),
        ("7th Sept against the third of May.", "seventh sept against the third of may"),
        (
            "Who is on first and what is on second.",
            "who is on first and what is on second",
        ),
        ("2001 a space Odyssey.", "two thousand and one a space odyssey"),
        (
            "I'm selling my car for one trillion.",
            "i 'm selling my car for one trillion",
        ),
        (
            "I'm selling my car for one trillion.",
            "i 'm selling my car for one trillion",
        ),
        (
            "I would recommend selling 2s 10s here.",
            "i would recommend selling twos tens here",
        ),
        ("129.6%.", "one hundred and twenty nine point six percent"),
        (
            "5.3% and then 129.6%.",
            "five point three percent and then one hundred and twenty nine point six percent",
        ),
        (
            "70.3% and coming around 129.6%.",
            "seventy point three percent and coming around one hundred and twenty nine point six percent",
        ),
        (
            "Dr. Joseph owes $12.5 billion.",
            "dr joseph owes twelve point five billion dollars",
        ),
        (
            "Replacements for things like Dr. for drive should only happen where necessary.",
            "replacements for things like dr for drive should only happen where necessary",
        ),
        ("100.", "one hundred"),
        ("115.", "one hundred and fifteen"),
        ("125.", "one hundred and twenty five"),
        ("140.", "one hundred and forty"),
        ("1000.", "one thousand"),
        ("1 2 3 4 5 6 7 8 9 10.", "one two three four five six seven eight nine ten"),
        (
            "his license plate is a. c, f seven...five ! zero",
            "his license plate is a c f seven five zero",
        ),
        ("Q2", "q two"),
        (
            "from our website at www.take2games.com.",
            "from our website at www take two games dot com",
        ),
        ("NBA 2K18", "n b a two k eighteen"),
        ("launched WWE 2K 18", "launched w w e two k eighteen"),
        (
            "released L.A. Noire, the The VR Case Files for the HTC VIVE system",
            "released l a noire the the v r case files for the h t c v i v e system",
        ),
        (
            "Total net bookings were $654 million,",
            "total net bookings were six hundred and fifty four million dollars",
        ),
        (
            "net booking which grew 6% to $380 million.",
            "net booking which grew six percent to three hundred and eighty million dollars",
        ),
        (
            "to $25 dollars or $0.21 per share price.",
            "to twenty five dollars dollars or zero dollars and twenty one cents per share price",
        ),
        ("year-over-year", "year over year"),
        ("HTC VIVE", "h t c v i v e"),
    ]

    for test in tests:
        input_string = test[0]
        result = clean_up(input_string)
        assert result == test[1]


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
