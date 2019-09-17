# Exercism Python Test Runner

The Docker image to automatically run tests on Python solutions submitted to [exercism](https://exercism.io).

## Running the Tests
To run a solution's tests, do the following:
1. Open termnial in project's root
2. Run `./run.sh <exercise-slug> <path-to-solution-folder>`


## Running the Tests in Docker container
*This script is provided for testing purposes*

To run a solution's test in the Docker container, do the following:
1. Open terminal in project's root
2. Run `./run-in-docker.sh <exercise-slug> <relative-path-to-solution-folder>`


### Known issues
* The output format of the tests is the default `pytest` format, since a standard is still not set at [exercism automated tests](https://github.com/exercism/automated-tests).

### Dummy

Dummy content to create PR that forces Github Actions check to run.
