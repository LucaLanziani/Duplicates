from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.fs.directory import Directory, DirNotFoundError
from nose.tools import eq_, raises

DIRECTORY = './test/files/test_dir_1'


class DirectoryTest(unittest.TestCase):

    # def setUp(self):
    #     self._dir = Directory('./test/files')

    @raises(DirNotFoundError)
    def test_non_existent_directory(self):
        list(Directory.content('./non-existent-directory'))

    def test_dir_content(self):
        eq_(len(list(Directory.content(DIRECTORY))), 3)

    def test_dir_content_limit(self):
        eq_(len(list(Directory.content(DIRECTORY, limit=1))), 1)

    def test_dir_content_zero_limit(self):
        eq_(len(list(Directory.content(DIRECTORY, limit=0))), 0)

    def test_dir_content_negative_limit(self):
        eq_(len(list(Directory.content(DIRECTORY, limit=-1))), 0)
