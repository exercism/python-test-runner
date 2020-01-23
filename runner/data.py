"""
Datatypes to support the Python test runner.
"""
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from json import JSONEncoder, dumps
from typing import Any, List, NewType, Optional
from pathlib import Path

# an exercise slug, ie two-fer
Slug = NewType("Slug", str)

# a directory
Directory = NewType("Directory", Path)

# a Pytest-style hierarchy, ./file.py::Class::test_function
Hierarchy = NewType("Hierarchy", str)


class Status(Enum):
    """
    The status of a given test or test session.
    """

    PASS = auto()
    FAIL = auto()
    ERROR = auto()


# a (optional) message for inclusion in results.json
Message = Optional[str]
Output = Optional[str]


@dataclass
class Test:
    """
    An individual test's results.
    """

    name: str
    status: Status = Status.PASS
    message: Message = None

    # for an explanation of why both of these are necessary see
    # https://florimond.dev/blog/articles/2018/10/reconciling-dataclasses-and-properties-in-python/
    output: Output = None
    _output: Output = field(default=None, init=False, repr=False)

    def _update(self, status: Status, message: Message = None) -> None:
        self.status = status
        if message:
            self.message = message

    @property
    def output(self) -> Output:
        return self._output

    @output.setter
    def output(self, captured: Output) -> None:

        # this test is necessary due to a curious artifact of @dataclass when
        # combined with @property; if no value is passed to the Test constructor
        # then the generated __init__ will attempt to call the property.setter
        # with the property itself; by ignoring that we let the private field's 
        # default value (in this case None) remain in place
        if isinstance(captured, property):
            return

        captured = captured.strip()
        truncate_msg = " [Output was truncated. Please limit to 500 chars]"
        if len(captured) > 500:
            captured = captured[: 500 - len(truncate_msg)] + truncate_msg
        self._output = captured

    def fail(self, message: Message = None) -> None:
        """
        Indicate this test failed.
        """
        self._update(Status.FAIL, message)

    def error(self, message: Message = None) -> None:
        """
        Indicate this test encountered an error.
        """
        self._update(Status.ERROR, message)

    def is_passing(self):
        """
        Check if the test is currently passing.
        """
        return self.status is Status.PASS


@dataclass
class Results:
    """
    Overall results of a test run.
    """

    status: Status = Status.PASS
    message: Message = None
    tests: List[Test] = field(default_factory=list)

    def add(self, test: Test) -> None:
        """
        Add a Test to the list of tests.
        """
        if test.status is Status.FAIL:
            self.fail()
        self.tests.append(test)

    def fail(self) -> None:
        """
        Indicate the test run had at least one failure.
        """
        self.status = Status.FAIL

    def error(self, message: Message = None) -> None:
        """
        Indicate the test run fatally errored.
        """
        self.status = Status.ERROR
        self.message = message

    @staticmethod
    def _factory(items):
        result = {}
        for k, v in items:
            if k == "_output" or k in {"message", "output"} and v is None:
                continue
            if isinstance(v, Status):
                v = v.name.lower()
            result[k] = v
        return result

    def as_json(self):
        """
        Dump the current Results to formatted JSON.
        """
        return dumps(asdict(self, dict_factory=self._factory), indent=2)
