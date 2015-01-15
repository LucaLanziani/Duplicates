from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.directory import Directory, DirNotFoundError
from nose.tools import assert_greater, eq_, raises


class DirectoryTest(unittest.TestCase):

    def setUp(self):
        self._dir = Directory('./test/files')

    @raises(DirNotFoundError)
    def non_existent_directory_test(self):
        Directory('./non-existent-directory')

    def absolute_directory_test(self):
        eq_(self._dir.pathname, os.path.abspath('./test/files'))

    def dir_content_test(self):
        eq_(len(list(self._dir.dir_content())), 2)

    def dir_content_filter_test(self):
        def pathname_filter(pathname):
            return pathname.endswith('.test')
        content = self._dir.dir_content(pathname_filter=pathname_filter)
        eq_(len(list(content)), 1)

    def dir_content_limit_test(self):
        eq_(len(list(self._dir.dir_content(limit=1))), 1)

    def dir_content_zero_limit_test(self):
        eq_(len(list(self._dir.dir_content(limit=0))), 0)

    def dir_content_negative_limit_test(self):
        eq_(len(list(self._dir.dir_content(limit=-1))), 0)

    def dir_content_total_filter_test(self):
        content = self._dir.dir_content(pathname_filter=lambda x: False)
        eq_(len(list(content)), 0)

    def _list_init_files(self, recursive):
        def pathname_filter(pathname):
            return pathname.endswith('__init__.py')
        directory = Directory('.')
        return list(directory.dir_content(recursive=recursive,
                                          pathname_filter=pathname_filter))

    def dir_content_non_recursive_test(self):
        eq_(len(self._list_init_files(False)), 0)

    def dir_content_recursive_test(self):
        assert_greater(len(self._list_init_files(True)), 0)
