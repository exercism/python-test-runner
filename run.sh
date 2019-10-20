#!/usr/bin/env bash

# Synopsis:
# Automatically tests exercism's Python track solutions against corresponding test files.
# Takes three arguments and makes sure all the tests are run

# Arguments:
# $1: exercise slug
# $2: path to solution folder (with trailing slash)
# $3: path to output directory (with trailing slash)

# Output:
# [For now] writes the tests output to the terminal

# Example:
# ./run.sh two-fer path/to/two-fer/solution/folder/ path/to/output/directory/


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
echo "Converting JUnit output to Exercism schema..."
python process_results.py results.xml results.json

# Reorder test cases by appearance in test file;
# pytest sorts cases alphabetically when running/reporting
echo "Sorting test results by appearance in test file..."
python sort_cases.py -v -o "$3results.json" "$test_file" results.json
