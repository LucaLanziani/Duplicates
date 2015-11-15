# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os

from duplicates.utils import absolute_path, DuplicateExceptions


class DirNotFoundError(DuplicateExceptions):
    pass


class Directory(object):
    """Describe a directory"""

    def __init__(self, path):
        super(Directory, self).__init__()
        self._directory = absolute_path(path)
        if not os.path.isdir(self._directory):
            raise DirNotFoundError(self._directory)

    def dir_content(self, recursive=True, limit=float("inf"),
                    pathname_filter=None):
        """
        yield white-listed files in the passed directory

        Args:
            recursive: navigate recursively all the directory tree
            limit: limit the number of files return by this function
            pathname_filter: a function that takes a pathname in input
                             and returns True or False
        """
        if pathname_filter is None:
            def true(pathname):
                return True
            pathname_filter = true

        for pathname in self._dir_content(recursive):
            limit -= 1
            if limit < 0:
                break
            if pathname_filter(pathname):
                yield pathname

    def _dir_content(self, recursive=True):
        dir_name = self._directory
        for root, dirs, files in os.walk(unicode(dir_name)):
            for name in files:
                yield os.path.join(root, name)
            if not recursive:
                break

    @property
    def pathname(self):
        return self._directory
