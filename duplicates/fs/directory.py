# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from duplicates.libraries.utils import absolute_path, DuplicateExceptions


class DirNotFoundError(DuplicateExceptions):
    pass


class Directory(object):
    """Describe a directory"""

    @classmethod
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
        if not os.path.isdir(directory):
            raise DirNotFoundError(directory)

        for pathname in cls._content(directory, recursive):
            limit -= 1
            if limit < 0:
                break
            yield directory, pathname

    @classmethod
    def _content(cls, directory, recursive=True):
        for root, dirs, files in os.walk(unicode(directory)):
            for name in files:
                yield os.path.join(root, name)
            if not recursive:
                break

if __name__ == '__main__':
    for directory, path in Directory.content('.'):
        print(directory, path)
