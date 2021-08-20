#!/usr/bin/env bash
test_dir="$(dirname "${BASH_SOURCE[0]}")"
python3 -m pytest -vv --doctest-modules $test_dir/../
