"""
Misc utils to support the Python test runner.
"""

import errno
import os
import re
from pathlib import Path

from .data import Slug, Directory


def slug(string: str) -> Slug:
    """
    Check if the given arg is a valid exercise slug.
    """
    pattern = r"^[a-z]+(-[0-9a-z]+)*$"
    if not re.match(pattern, string):
        raise ValueError(f"Does not match {pattern!r}: {string!r}")
    return Slug(string)


def directory(string: str) -> Directory:
    """
    Check if the given arg is a readable / writeable directory.
    """
    path = Path(string)
    if not path.is_dir():
        err = errno.ENOENT
        msg = os.strerror(err)
        raise FileNotFoundError(err, f"{msg}: {string!r}")

    if not os.access(path, os.R_OK | os.W_OK):
        err = errno.EACCES
        msg = os.strerror(err)
        raise PermissionError(err, f"{msg}: {string!r}")
    return Directory(path)
