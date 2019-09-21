#!/usr/bin/env bash

# Synopsis:
# Test runner for run.sh in a docker container
# Takes the same arguments as run.sh (EXCEPT THAT SOLUTION PATH IS RELATIVE)
# Builds the Dockerfile
# Runs the docker image passing along the initial arguments

# Arguments:
# $1: exercise slug
# $2: **RELATIVE** path to solution folder (with trailing slash)

# Output:
# [For now] writes the tests output to the terminal

# Example:
# ./run-in-docker.sh two-fer ./relative/path/to/two-fer/solution/folder/

# If arguments not provided, print usage and exit
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "usage: run-in-docker.sh exercise-slug ./relative/path/to/solution/folder/"
    exit 1
fi

# build docker image
docker build -t python-test-runner .

# run image passing the arguments
docker run -v $PWD/$2:/solution python-test-runner $1 /solution/
