#! /usr/bin/env python3
"""
CLI for the test runner for the Python track on Exercism.io.
"""
from argparse import ArgumentParser, ArgumentTypeError, REMAINDER

import runner


def _slug(arg):
    try:
        return runner.utils.slug(arg)
    except ValueError as err:
        raise ArgumentTypeError(str(err))


def _directory(arg):
    try:
        return runner.utils.directory(arg)
    except (FileNotFoundError, PermissionError) as err:
        raise ArgumentTypeError(str(err))


def main():
    """
    Parse CLI arguments and run the tests.
    """
    parser = ArgumentParser(
        description="Run the tests of a Python exercise."
    )

    parser.add_argument(
        "slug", metavar="SLUG", type=_slug, help="name of the exercise to process",
    )

    parser.add_argument(
        "input",
        metavar="IN",
        type=_directory,
        help="directory where the [EXERCISE.py] file is located",
    )

    parser.add_argument(
        "output",
        metavar="OUT",
        type=_directory,
        help="directory where the results.json will be written",
    )

    parser.add_argument("pytest_args", nargs=REMAINDER)

    args = parser.parse_args()
    runner.run(args.slug, args.input, args.output, args.pytest_args)


if __name__ == "__main__":
    main()
