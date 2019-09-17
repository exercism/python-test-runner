#!/usr/bin/env python
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def _process_xml_tree(tree):
    results = {
        'status': 'pass',
        'message': None,
        'tests': []
    }
    root = tree.getroot()
    for testcase in root.findall('*/testcase'):
        case = {
            'name': testcase.attrib['name'],
            'status': 'pass'
        }
        error = testcase.find('./error')
        failure = testcase.find('./failure')
        if error is not None:
            results['status'] = 'error'
            case['status'] = 'error'
            case['message'] = error.attrib['message']
        elif failure is not None:
            # Don't allow subsequent failures to clobber error status
            if results['status'] != 'error':
                results['status'] = 'fail'
            case['status'] = 'fail'
            case['message'] = failure.attrib['message']
        results['tests'].append(case)
    return results


def _write_output_file(results, output_path):
    if output_path == '-':
        print(json.dumps(results, indent=2))
    else:
        with open(output_path, 'w') as f:
            f.write(json.dumps(results))


def convert_junitxml_to_json(xml_path, output_path):
    tree = ET.parse(xml_path)
    results = _process_xml_tree(tree)
    _write_output_file(results, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_path', type=Path, help='JUnit XML report file')
    parser.add_argument(
        'output_path',
        nargs='?',
        default='-',
        help='JSON output path'
    )
    opts = parser.parse_args()
    convert_junitxml_to_json(opts.xml_path, opts.output_path)
