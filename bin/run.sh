#! /bin/sh
root="$( dirname "$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )" )"
export PYTHONPATH="$root:$PYTHONPATH"
python bin/run.py "$@"
