"""
Representer for Python.
"""
import time
from json import dumps
from typing import Dict, List

import pytest

from . import utils


import ast
import os

class TestOrderVisitor(ast.NodeVisitor):
    """
    Visits test_* methods and caches their definition order.
    """

    _cache = {}

    def __init__(self, name):
        super().__init__()
        self._hierarchy = [name]

    def visit_ClassDef(self, node):
        """
        Handles class definitions.
        """
        bases = {f"{b.value.id}.{b.attr}" for b in node.bases}
        if "unittest.TestCase" in bases:
            self._hierarchy.append(node.name)
        self.generic_visit(node)
        self._hierarchy.pop()

    def visit_FunctionDef(self, node):
        """
        Handles function definitions
        """
        if node.name.startswith("test_"):
            self._cache[self.get_hierarchy(node.name)] = node.lineno
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def get_hierarchy(self, name):
        """
        Returns the hierarchy :: joined.
        """
        return "::".join(self._hierarchy + [name])

    @staticmethod
    def definition_order(node):
        """
        Returns the line the given node was defined on.
        """
        if node.nodeid not in TestOrderVisitor._cache:
            with open(node.fspath, "r") as src:
                tree = ast.parse(src.read(), os.path.basename(node.fspath))
            TestOrderVisitor(node.nodeid.split("::")[0]).visit(tree)
        return TestOrderVisitor._cache[node.nodeid]

from dataclasses import dataclass, field, asdict
from typing import NewType, Optional

Status = NewType("Status", str)

PASS = Status("pass")
FAIL = Status("fail")
ERROR = Status("error")

@dataclass
class Test:
    name: str
    status: Status
    message: Optional[str] = None

@dataclass
class Results:
    status: Status = PASS
    message: Optional[str] = None
    tests: List[Test] = field(default_factory=list)

    def add(self, name: str, status: Status, message: Optional[str] = None):
        self.tests.append(Test(name, status, message))

class ResultsReporter:
    def __init__(self):
        self.report = Results()
        self.tests = {}
        self.last_err = None

    def pytest_collection_modifyitems(self, session, config, items):
        """
        Sorts the tests in definition order.
        """
        items.sort(key=TestOrderVisitor.definition_order)

    def pytest_runtest_logreport(self, report):
        """
        Process a test setup / call / teardown report.
        """
        name = ".".join(report.nodeid.split("::")[1:])
        if name not in self.tests:
            self.tests[name] = Test(name, PASS)
        state = self.tests[name]

        # ignore succesful setup and teardown stages
        if report.passed and report.when != "call":
            return

        # do not update tests that have already failed
        if state.status != PASS:
            return

        # determine failure state
        if report.failed:
            state.status = FAIL
            if report.when != "call":
                state.status = ERROR

        if report.longrepr:
            crash = report.longrepr.reprcrash
            state.message = f"{crash.lineno}: {crash.message}"


    def pytest_sessionfinish(self, session, exitstatus):
        """
        Processes the results into a report.
        """
        exitcode = pytest.ExitCode(int(exitstatus))
        if exitcode is pytest.ExitCode.TESTS_FAILED:
            self.report.status = FAIL
        elif exitcode is not pytest.ExitCode.OK:
            self.report.status = ERROR
            if self.last_err is not None:
                self.report.message = self.last_err
            if self.report.message is None:
                self.report.message = f"Unexpected ExitCode.{exitcode.name}: check logs for details"
        self.report.tests = list(self.tests.values())

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


def run(slug: utils.Slug, indir: utils.Directory, outdir: utils.Directory, args: List[str]) -> None:
    """
    Run the tests for the given exercise and produce a results.json.
    """
    test_file = indir.joinpath(slug.replace("-", "_") + "_test.py")
    out_file = outdir.joinpath("results.json")

    reporter = ResultsReporter()
    pytest.main(args + [str(test_file)], plugins=[reporter])

    # dump the results 
    out_file.write_text(dumps(asdict(reporter.report), indent=2))
