"""
Configures tests to run in the order in which they were defined.
"""
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
            TestOrderVisitor(os.path.basename(node.fspath)).visit(tree)
        return TestOrderVisitor._cache[node.nodeid]


def pytest_collection_modifyitems(session, config, items):
    """
    Sorts the tests in definition order.
    """
    items.sort(key=TestOrderVisitor.definition_order)
