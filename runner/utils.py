"""
Representer for Python.
"""
import errno
import os
import re
from pathlib import Path
from typing import NewType


Slug = NewType("Slug", str)

SLUG_RE = re.compile(r"^[a-z]+(-[0-9a-z]+)*$")


def slug(string: str) -> Slug:
    """
    Check if the given arg is a valid exercise slug.
    """
    if not SLUG_RE.match(string):
        raise ValueError(f"Does not match {SLUG_RE.pattern!r}: {string!r}")
    return Slug(string)


Directory = NewType("Directory", Path)


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

