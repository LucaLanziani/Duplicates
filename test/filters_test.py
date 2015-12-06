from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.lib.filters import BaseFilter, UnixShellWildcardsFilter
from nose.tools import eq_, raises


class BaseFilterTest(unittest.TestCase):

    def setUp(self):
        self.filter = BaseFilter()

    @raises(NotImplementedError)
    def test_match(self):
        self.filter.match('')


class UnixShellWildcardsFilterTest(unittest.TestCase):

    def _get_filter(self, *patterns):
        return UnixShellWildcardsFilter(*patterns)

    def test_asterisk_pattern(self):
        ufilter = self._get_filter('*')
        eq_(ufilter.match('/folder1/folder2/file'), True)

    def test_directory_match(self):
        ufilter = self._get_filter('*.git/*')
        eq_(ufilter.match('.git/config'), True)
        eq_(ufilter.match('/folder1/.git/file'), True)
        eq_(ufilter.match('/folder1/folder2/.git'), False)

    def test_file_match(self):
        ufilter = self._get_filter('*.gitignore')
        eq_(ufilter.match('.gitignore'), True)
        eq_(ufilter.match('/folder1/.gitignore'), True)
        eq_(ufilter.match('random_file'), False)
        eq_(ufilter.match('/folder/random_file'), False)

    def test_exact_matc(self):
        ufilter = self._get_filter('test')
        eq_(ufilter.match('test'), True)

    def test_multiple_patterns(self):
        ufilter = self._get_filter('test', '*test')
        eq_(ufilter.match('asdftest'), True)
        eq_(ufilter.match('test_file'), False)
