from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.indexer import Indexer
from nose.tools import eq_

TEST_DIR = './test/files/'


class DuplicatesTest(unittest.TestCase):

    def setUp(self):
        self.duplicates = Indexer(TEST_DIR)

    def test_collect_data(self):
        result = self.duplicates.index()
        eq_(len(result), 3)

    def test_empty_unix_patters(self):
        duplicates = Indexer(TEST_DIR, unix_patterns=[])
        result = duplicates.index()
        eq_(len(result), 3)

    def test_asterisk_unix_pattern(self):
        duplicates = Indexer(TEST_DIR, unix_patterns="*")
        result = duplicates.index()
        print(result)
        eq_(len(result), 3)
