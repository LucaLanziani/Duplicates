from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os

from utils import absolute_path


class Directory(object):
    """Describe a directory"""

    def __init__(self, path):
        super(Directory, self).__init__()
        self._directory = absolute_path(path)
        assert os.path.isdir(self._directory)

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
            pathname_filter = lambda pathname: True

        for pathname in self._dir_content(recursive):
            if pathname_filter(pathname):
                yield pathname

                limit -= 1
                if limit == 0:
                    break

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
