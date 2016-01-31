# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from fnmatch import fnmatch


class BaseFilter(object):

    def match(self, pathname):
        raise NotImplementedError


class UnixShellWildcardsFilter(BaseFilter):
    """Implements a filter that returns True if the pathname matches one of
    the patterns in the filter.

    The comparison is done using the fnmatch module that provides support
    for Unix shell-style wildcards
    """

    def __init__(self, *patterns):
        super(UnixShellWildcardsFilter, self).__init__()
        self._patterns = map(lambda pattern: pattern.lower(), patterns)
        if not self._patterns:
            self._patterns.append('*')

    def _match(self, pathname):
        """
        Return if name matches any of the patterns.
        """
        for pattern in self._patterns:
            if fnmatch(pathname.lower(), pattern):
                return True
        return False

    @property
    def enabled(self):
        return self._patterns

    def match(self, pathname):
        return self._match(pathname)

    def filter_dircontent(self, dircontent):
        for filepath, directory in dircontent:
            if self.match(filepath):
                yield filepath, directory
