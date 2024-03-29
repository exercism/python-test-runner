#! /bin/sh

root="/opt/test-runner"
export PYTHONPATH="$root:$PYTHONPATH"

mkdir autograding_output

while [ $# -gt 0 ]; do
  case "$1" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      ;;
    --max-score=*)
      MAX_SCORE="${1#*=}"
      ;;
    --setup-command=*)
      SETUP_COMMAND="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Warning: Unknown argument.*\n"
      printf "***************************\n"
  esac
  shift
done

echo "TIMEOUT is $TIMEOUT"
echo "MAX_SCORE is $MAX_SCORE"

if [ -n "$SETUP_COMMAND" ]; then
  echo "Running setup command: $SETUP_COMMAND"
  eval "$SETUP_COMMAND"
fi

python3 /opt/test-runner/bin/run.py ./ ./autograding_output/ "$MAX_SCORE" "$TIMEOUT"

echo "result=$(jq -c . autograding_output/results.json | jq -sRr @base64)" >> "$GITHUB_OUTPUT"
