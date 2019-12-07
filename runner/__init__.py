"""
Test Runner for Python.
"""
from typing import Dict, List, Optional
from pathlib import Path

import pytest

from .data import Slug, Directory, Hierarchy, Results, Test
from .sort import TestOrder

class ResultsReporter:
    def __init__(self):
        self.results = Results()
        self.tests = {}
        self.last_err = None

    def pytest_collection_modifyitems(self, session, config, items):
        """
        Sorts the tests in definition order.
        """
        def _sort_by_lineno(item):
            test_id = Hierarchy(item.nodeid)
            source = Path(item.fspath)
            return TestOrder.lineno(test_id, source)
        items.sort(key=_sort_by_lineno)

    def pytest_runtest_logreport(self, report):
        """
        Process a test setup / call / teardown report.
        """
        name = ".".join(report.nodeid.split("::")[1:])
        if name not in self.tests:
            self.tests[name] = Test(name)
        state = self.tests[name]

        # ignore succesful setup and teardown stages
        if report.passed and report.when != "call":
            return

        # do not update tests that have already failed
        if not state.is_passing():
            return

        # handle test failure
        if report.failed:
            message = None
            if report.longrepr:
                crash = report.longrepr.reprcrash
                message = f"{crash.lineno}: {crash.message}"
            
            # test failed due to a setup / teardown error
            if report.when != "call":
                state.error(message)
            else:
                state.fail(message)

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
        if report.longreprtext:
            self.last_err = report.longreprtext


def run_tests(path: Path, args: Optional[List[str]] = None) -> Results:
    """
    Run the tests and generate Results for inspection.
    """
    reporter = ResultsReporter()
    pytest.main(args or [] + [str(path)], plugins=[reporter])
    return reporter.results

def run(slug: Slug, indir: Directory, outdir: Directory, args: List[str]) -> None:
    """
    Run the tests for the given exercise and produce a results.json.
    """
    test_file = indir.joinpath(slug.replace("-", "_") + "_test.py")
    out_file = outdir.joinpath("results.json")
    # run the tests and report 
    results = run_tests(test_file, args)
    # dump the report
    out_file.write_text(results.as_json())
