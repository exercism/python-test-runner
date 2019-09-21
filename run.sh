#!/usr/bin/env bash

# Synopsis:
# Automatically tests exercism's Python track solutions against corresponding test files.
# Takes two arguments and makes sure all the tests are run

# Arguments:
# $1: exercise slug
# $2: path to solution folder (with trailing slash)

# Output:
# Writes a results.json file with the test results in the solution directory

# Example:
# ./run.sh two-fer path/to/two-fer/solution/folder/


pip3 install pytest

# Replace hyphen with underscore to follow Python snake-case filename convention
test_file="${1/-/_}"

# Put together path to the test file
test_file="$2$test_file"_test.py

# Run pytest and generate JUnit xml report
pytest --junitxml="results.xml" "$test_file"

# Convert JUnit report to results.json
# At some future date, this script should be replaced
# with one provided by exercism/automated-tests
python process_results.py results.xml "$2"results.json
