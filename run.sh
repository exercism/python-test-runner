#!/usr/bin/env bash
set -ex

# Synopsis:
# Automatically tests exercism's Python track solutions against corresponding test files.
# Takes three arguments and makes sure all the tests are run
# Writes the results to the output directory

# Arguments:
# $1: exercise slug
# $2: path to solution folder (with trailing slash)
# $3: path to output directory (with trailing slash)

# Output:
# Writes the test results to a results.json file in the passed-in output directory.
# The test results are formatted according to the specifications at https://github.com/exercism/automated-tests/blob/master/docs/interface.md

# Example:
# ./run.sh two-fer path/to/two-fer/solution/folder/ path/to/output/directory/

# Replace hyphen with underscore to follow Python snake-case filename convention
test_file="${1//-/_}"
solution_dir="$2"
output_dir="$3"

# Put together path to the test file
test_file="$2$test_file"_test.py

# Run pytest and generate JUnit xml report
pytest -v --junitxml="results.xml" "$test_file"

# Convert JUnit report to results.json
# At some future date, this script should be replaced
# with one provided by exercism/automated-tests
echo "Converting JUnit output to Exercism schema..."
python process_results.py results.xml "${output_dir}results.json"
