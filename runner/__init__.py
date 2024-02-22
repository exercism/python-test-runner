"""
Test Runner for Python.
"""
import os
import re
from textwrap import dedent
from typing import List
from pathlib import Path
import json
import shutil

import pytest

from .data import Directory, Hierarchy, Results, Test
from .sort import TestOrder


class ResultsReporter:
    def __init__(self):
        self.results = Results()
        self.tests = {}
        self.last_err = None
        self.config = None

    def pytest_configure(self, config):
        config.addinivalue_line("markers", "task(taskno): this marks the exercise task number.")
        self.config = config

    def pytest_collection_modifyitems(self, session, config, items):
        """
        Sorts the tests in definition order & extracts task_id
        """
        for item in items:
            test_id = Hierarchy(item.nodeid)
            name = '.'.join(test_id.split("::")[1:])

            for mark in item.iter_markers(name='task'):
                self.tests[name] = Test(name=name, task_id=mark.kwargs['taskno'])


        def _sort_by_lineno(item):
            test_id = Hierarchy(item.nodeid)
            source = Path(item.fspath)
            return TestOrder.lineno(test_id, source)

        items.sort(key=_sort_by_lineno)

    def pytest_runtest_logreport(self, report):
        """
        Process a test setup / call / teardown report.
        """

        name = report.head_line if report.head_line else ".".join(report.nodeid.split("::")[1:])
        if name not in self.tests:
            # Extract filename and line number
            filename = report.location[0]
            line_no = report.location[1]
            # Initialize Test with filename and line number
            self.tests[name] = Test(name, filename=filename, line_no=line_no)

        state = self.tests[name]

        # Store duration
        state.duration = report.duration

        # ignore successful setup and teardown stages
        if report.passed and report.when != "call":
            return

        # Update tests that have already failed with capstdout and return.
        if not state.is_passing():
            if report.capstdout.rstrip('FFFFFFFF ').rstrip('uuuuu'):
                state.output = report.capstdout.rstrip('FFFFFFFF ').rstrip('uuuuu')
            return

        # Record captured relevant stdout content for passed tests.
        if report.capstdout:
            state.output = report.capstdout

        # Handle details of test failure
        if report.failed:

            # traceback that caused the issued, if any
            message = None
            if report.longrepr:
                trace = report.longrepr.reprtraceback
                crash = report.longrepr.reprcrash
                message = self._make_message(trace, crash)

            # test failed due to a setup / teardown error
            if report.when != "call":
                state.error(message)
            else:
                state.fail(message)

        test_id = Hierarchy(report.nodeid)
        source = Path(self.config.rootdir) / report.fspath
        state.test_code = TestOrder.function_source(test_id, source)


        # Looks up test_ids from parent when the test is a subtest.
        if state.task_id == 0 and 'variation' in state.name:
            parent_test_name = state.name.split(' ')[0]
            parent_task_id = self.tests[parent_test_name].task_id
            state.task_id = parent_task_id


            # Changes status of parent to fail if any of the subtests fail.
            if state.fail:
                self.tests[parent_test_name].fail(
                    message="One or more variations of this test failed. Details can be found under each [variant#]."
                )
                self.tests[parent_test_name].test_code = state.test_code


    def pytest_sessionfinish(self, session, exitstatus):
        """
        Processes the results into a report.
        """
        exitcode = pytest.ExitCode(int(exitstatus))

        # at least one of the tests has failed
        if exitcode is pytest.ExitCode.TESTS_FAILED:
            self.results.fail()

        # an error has been encountered
        elif exitcode is not pytest.ExitCode.OK:
            message = None
            if self.last_err is not None:
                message = self.last_err
            else:
                message = f"Unexpected ExitCode.{exitcode.name}: check logs for details"
            self.results.error(message)

        for test in self.tests.values():
            self.results.add(test)

    def pytest_terminal_summary(self, terminalreporter):
        """
        Report to the terminal that the reporter has run.
        """
        terminalreporter.write_sep("-", "generated results.json")

    def pytest_exception_interact(self, node, call, report):
        """
        Catch the last exception handled in case the test run itself errors.
        """
        if report.outcome == "failed":
            excinfo = call.excinfo
            err = excinfo.getrepr(style="no", abspath=False)

            # trim off full traceback for first two exercises to be friendlier and clearer
            if ('lasagna' in node.name or 'hello_world' in node.name) and 'ImportError' in str(err.chain[0]):
                trace = err.chain[-2][0]
            else:
                trace = err.chain[-1][0]

            crash = err.chain[0][1]
            self.last_err = self._make_message(trace, crash)

    def _make_message(self, trace, crash=None):
        """
        Make a formatted message for reporting.
        """

        # stringify the traceback, strip pytest-specific formatting
        message = dedent(re.sub("^E |_pytest.nodes.Collector.CollectError: ", "  ", str(trace), flags=re.M))

        # if a path exists that's relative to the runner we can strip it out
        if crash:
            common = os.path.commonpath([Path.cwd(), Path(crash.path)])
            message = message.replace(common, ".")
        return message


def _sanitize_args(args: List[str]) -> List[str]:
    clean = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg == "--tb":
            skip_next = True
            continue
        elif arg.startswith("--tb="):
            continue
        clean.append(arg)
    clean.append("--tb=no")
    return clean


def run(indir: Directory, outdir: Directory, args: List[str]) -> None:
    """
    Run the tests for the given exercise and produce a results.json.
    """
    test_files = []

    for root, dirs, files in os.walk(indir):
        for file in files:
            if file.endswith("_test.py"):
                test_files.append(Path(root) / file)

    out_file = outdir.joinpath("results.json")

    # run the tests and report
    reporter = ResultsReporter()
    pytest.main(_sanitize_args(args or []) + [str(tf) for tf in test_files], plugins=[reporter])

    # dump the report
    out_file.write_text(reporter.results.as_json())
    # remove cache directories
    for cache_dir in ['.pytest_cache', '__pycache__']:
        dirpath = indir / cache_dir
        if dirpath.is_dir():
            shutil.rmtree(dirpath)
