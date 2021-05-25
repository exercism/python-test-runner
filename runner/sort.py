"""
Test Runner for Python.
"""
from ast import (
    NodeVisitor,
    ClassDef,
    FunctionDef,
    AsyncFunctionDef,
    parse,
    For,
    While,
    If
)
from pathlib import Path
from typing import Dict, overload

from .data import Hierarchy, TestInfo

# pylint: disable=invalid-name, no-self-use


class TestOrder(NodeVisitor):
    """
    Visits test_* methods in a file and caches their definition order.
    """

    _cache: Dict[Hierarchy, TestInfo] = {}

    def __init__(self, root: Hierarchy) -> None:
        super().__init__()
        self._hierarchy = [root]

    def visit_ClassDef(self, node: ClassDef) -> None:
        """
        Handles class definitions.
        """
        bases = {f"{base.value.id}.{base.attr}" for base in node.bases}

        if "unittest.TestCase" in bases:
            self._hierarchy.append(Hierarchy(node.name))

        self.generic_visit(node)
        self._hierarchy.pop()

    @overload
    def _visit_definition(self, node: FunctionDef) -> None:
        ...

    @overload
    def _visit_definition(self, node: AsyncFunctionDef) -> None:
        ...

    def _visit_definition(self, node):
        if node.name.startswith("test_"):
            last_body = node.body[-1]

            while isinstance(last_body, (For, While, If)):
                last_body = last_body.body[-1]


            testinfo = TestInfo(node.lineno, last_body.lineno, 1)
            self._cache[self.get_hierarchy(Hierarchy(node.name))] = testinfo

        self.generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef) -> None:
        """
        Handles test definitions
        """
        self._visit_definition(node)

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef) -> None:
        """
        Handles async test definitions
        """
        self._visit_definition(node)

    def get_hierarchy(self, name: Hierarchy) -> Hierarchy:
        """
        Returns the hierarchy :: joined.
        """
        return Hierarchy("::".join(self._hierarchy + [name]))


    @classmethod
    def lineno(cls, test_id: Hierarchy, source: Path) -> int:
        """
        Returns the line that the given test was defined on.
        """
        if test_id not in cls._cache:
            tree = parse(source.read_text(), source.name)
            cls(Hierarchy(test_id.split("::")[0])).visit(tree)
        return cls._cache[test_id].lineno


    @classmethod
    def function_source(cls, test_id: Hierarchy, source: Path) -> str:
        """
        Returns the source code of the given test.
        """
        text = source.read_text()
        testinfo = cls._cache[test_id]
        lines = text.splitlines()[testinfo.lineno: testinfo.end_lineno + 1]

        if test_id not in cls._cache:
            tree = parse(text, source.name)
            cls(Hierarchy(test_id.split("::")[0])).visit(tree)

        if not lines[-1]:
            lines.pop()

        # dedent source
        while all(line.startswith(' ') for line in lines if line):
            lines = [line[1:] if line else line for line in lines]
        return '\n'.join(lines)
