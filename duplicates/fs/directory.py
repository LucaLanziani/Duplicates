# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from duplicates.libraries.utils import absolute_path, DuplicateExceptions


class DirNotFoundError(DuplicateExceptions):
    pass


def dir_exists(func):
    def func_wrapper(cls, pathname, *args, **kwargs):
        abs_pathname = absolute_path(pathname)
        if not os.path.isdir(abs_pathname):
            raise DirNotFoundError(abs_pathname)
        return func(cls, pathname, *args, **kwargs)
    return func_wrapper


class Directory(object):
    """Describe a directory"""

    @classmethod
    @dir_exists
    def content(cls, path, recursive=True, limit=float("inf")):
        """
        yield white-listed files in the passed directory

        Args:
            recursive: navigate recursively all the directory tree
            limit: limit the number of files return by this function
            pathname_filter: a function that takes a pathname in input
                             and returns True or False
        """
        directory = absolute_path(path)
        for pathname in cls._content(directory, recursive):
            limit -= 1
            if limit < 0:
                break
            yield directory, os.path.relpath(pathname, directory)

    @classmethod
    @dir_exists
    def _content(cls, directory, recursive=True):
        for root, dirs, files in os.walk(unicode(directory)):
            for name in files:
                yield os.path.join(root, name)
            if not recursive:
                break

if __name__ == '__main__':
    for directory, path in Directory.content('.'):
        print(directory, path)
