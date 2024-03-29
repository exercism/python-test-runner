#! /bin/sh

root="/opt/test-runner"
export PYTHONPATH="$root:$PYTHONPATH"

mkdir autograding_output

while [ $# -gt 0 ]; do
  case "$1" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      ;;
    --max_score=*)
      MAX_SCORE="${1#*=}"
      ;;
    --setup_command=*)
      SETUP_COMMAND="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Warning: Unknown argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

echo "TIMEOUT is $TIMEOUT"
echo "MAX_SCORE is $MAX_SCORE"
echo "SETUP_COMMAND is $SETUP_COMMAND"

python3 /opt/test-runner/bin/run.py ./ ./autograding_output/ "$MAX_SCORE" "$TIMEOUT"

echo "result=$(jq -c . autograding_output/results.json | jq -sRr @base64)" >> "$GITHUB_OUTPUT"
