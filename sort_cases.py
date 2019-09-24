#!/usr/bin/env python
import argparse
import json
import logging
import re
from pathlib import Path


logging.basicConfig()


RGX_TEST_DEFINITION = re.compile(r'^def (?P<name>test_[^(]+)')


def create_cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('test_file', type=Path)
    parser.add_argument('results_file', type=Path)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-o', '--output', default='-')
    return parser


def get_tests(test_file):
    logging.info(f'loading test order from {test_file}')
    with open(test_file) as f:
        return {
            match.group('name'): i
            for i, match in enumerate(
                RGX_TEST_DEFINITION.match(line.strip())
                for line in f.readlines()
            )
            if match is not None
        }


def load_results(results_file):
    logging.info(f'loading results from {results_file}')
    with open(results_file) as f:
        return json.load(f)


def sort_results(ordered_tests, results):
    logging.info('sorting tests')
    sorted_results = dict(results)
    sorted_results['tests'] = sorted(
        results['tests'], key=lambda t: ordered_tests[t['name']]
    )
    return sorted_results


if __name__ == '__main__':
    opts = create_cli_parser().parse_args()
    if opts.verbose:
        logging.basicConfig(level=logging.INFO)
    ordered_tests = get_tests(opts.test_file)
    results = load_results(opts.results_file)
    sorted_results = sort_results(ordered_tests, results)
    output_content = json.dumps(sorted_results, indent=2)
    if opts.output == '-':
        print(output_content)
    else:
        output_path = Path(opts.output)
        with open(output_path, 'w') as f:
            f.write(output_content)
        logging.info(f'sorted results written to {opts.output}')
