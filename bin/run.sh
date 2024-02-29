#! /bin/sh

root="/opt/test-runner"
export PYTHONPATH="$root:$PYTHONPATH"

mkdir autograding_output

MAX_SCORE="$1"

echo "max score is $MAX_SCORE"

python3 /opt/test-runner/bin/run.py ./ ./autograding_output/ "$MAX_SCORE"

echo "result=$(jq -c . autograding_output/results.json | jq -sRr @base64)" >> "$GITHUB_OUTPUT"
