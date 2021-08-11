#!/usr/bin/env python
"""
Test xlsx extraction
"""

import os

from asrtoolkit.extract_excel_spreadsheets import proc_input_dir_to_corpus

from utils import get_test_dir

test_dir = get_test_dir(__file__)


def test_excel_conversion():
    " execute single test "

    proc_input_dir_to_corpus("samples", f"{test_dir}/corpus")
    assert os.path.exists(f"{test_dir}/corpus/FinancialStatementFY18Q4.txt")


if __name__ == "__main__":
    import sys

    import pytest

    pytest.main(sys.argv)
