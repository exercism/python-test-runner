#!/usr/bin/env bash

# Synopsis:
# Automatically tests exercism's Python track solutions against corresponding test files.
# Takes two arguments and makes sure all the tests are run

# Arguments:
# $1: exercise slug
# $2: path to solution folder (without trailing slash)

# Output:
# [For now] writes the tests output to the terminal

# Example:
# ./run.sh two-fer path/to/two-fer/solution/folder


pip3 install pytest

# Replace hyphen with underscore to follow Python snake-case filename convention
test_file="${1/-/_}"

# Put together path to the test file
test_file="$2/$test_file"_test.py

pytest --exitfirst "$test_file"