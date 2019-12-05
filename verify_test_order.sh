#!/bin/bash
set -e

EXERCISE_SLUG="$1"
SOLUTION_DIR="$2"
OUTPUT_DIR="$3"

TEST_FILE="$2/${1//-/_}_test.py"
RESULTS_FILE="$3/results.json"

from_test_file()
{
    grep -oP '(?<=def )(test_[^(]+)' "$TEST_FILE"
}

from_results_file()
{
    PYTHON_CODE=$(cat <<EOF
import json
import sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for test in data['tests']:
    print(test['name'])

EOF
)
    python -c "$PYTHON_CODE" "$RESULTS_FILE"
}
# echo "$TEST_FILE"
# # from_test_file
diff <(from_test_file) <(from_results_file)
