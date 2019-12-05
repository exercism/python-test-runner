import pytest
from itertools import groupby
from functools import partial
import re

RGX_TEST_NAME = re.compile(r"^(?P<indent>\s*)def (?P<name>test_[^(]+)\(.*")
RGX_TEST_CLASS = re.compile(r"^class (?P<name>[^(:]+)[(:]")


class ClassIndex:
    def __init__(self, name, line_no):
        self.name = name
        self.line_no = line_no
        self.__tests__ = {}

    def __getitem__(self, key):
        return self.__tests__[key]

    def __setitem__(self, key, value):
        self.__tests__[key] = value


class FileIndex:
    @classmethod
    def create(cls, fspath, position=0):
        file_index = cls(fspath, position)
        current_class = file_index[None]
        with open(fspath) as f:
            for line_no, line in enumerate(f, start=1):
                m = RGX_TEST_CLASS.match(line)
                if m is not None:
                    current_class = file_index.create_class_index(
                        m.group("name"), line_no
                    )
                else:
                    m = RGX_TEST_NAME.match(line)
                    if m is not None:
                        test_name = m.group("name")
                        if len(m.group("indent")) == 0:
                            current_class = file_index[None]
                        current_class[test_name] = line_no
        return file_index

    def __init__(self, fspath, position=0):
        self.fspath = fspath
        self.position = position
        self.__classes__ = {}
        self.create_class_index(None, 0)

    def create_class_index(self, classname, line_no):
        index = ClassIndex(classname, line_no)
        self.__classes__[classname] = index
        return index

    def __getitem__(self, key):
        return self.__classes__[key]


def get_test_sort_key(index_by_file, test_item):
    file_index = index_by_file.get(test_item.fspath, None)
    if file_index is None:
        file_index = FileIndex.create(test_item.fspath, len(index_by_file))
        index_by_file[test_item.fspath] = file_index
    if test_item.parent is None:
        parent_name = None
    else:
        parent_name = test_item.parent.name
    return (
        file_index.position,
        file_index[parent_name].line_no,
        file_index[parent_name][test_item.name],
    )


def pytest_collection_modifyitems(items):
    print("\nsorting by appearance in source file...")
    index_by_file = {}
    items.sort(key=partial(get_test_sort_key, index_by_file))
