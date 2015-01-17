from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.filters import UnixShellWildcardsFilter

from nose.tools import eq_


class UnixShellWildcardsFilterTest(unittest.TestCase):

    def _get_filter(self, patterns):
        return UnixShellWildcardsFilter(patterns)

    def test_simple_pattern(self):
        ufilter = self._get_filter(['*'])
        eq_(ufilter.match('/folder1/folder2/file'), True)

    def test_directory_match(self):
        ufilter = self._get_filter(['*.git/*'])
        eq_(ufilter.match('.git/config'), True)
        eq_(ufilter.match('/folder1/.git/file'), True)
        eq_(ufilter.match('/folder1/folder2/.git'), False)

    def test_file_match(self):
        ufilter = self._get_filter(['*.gitignore'])
        eq_(ufilter.match('.gitignore'), True)
        eq_(ufilter.match('/folder1/.gitignore'), True)
