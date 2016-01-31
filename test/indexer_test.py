from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.indexer import Indexer
from nose.tools import eq_

TEST_DIR = './test/files/test_dir_1/'


class IndexerTest(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer(TEST_DIR)

    def test_collect_data(self):
        result = self.indexer.index()
        eq_(len(result), 3)

    def test_empty_unix_patters(self):
        indexer = Indexer(TEST_DIR, unix_patterns=[])
        result = indexer.index()
        eq_(len(result), 3)

    def test_asterisk_unix_pattern(self):
        indexer = Indexer(TEST_DIR, unix_patterns="*")
        result = indexer.index()
        eq_(len(result), 3)

    def test_unix_patters(self):
        indexer = Indexer(TEST_DIR, unix_patterns=['*.jpg', '*.test'])
        result = indexer.index()
        eq_(len(result), 2)

    def test_double_run(self):
        indexer = Indexer(TEST_DIR, unix_patterns=['*.jpg', '*.test'])
        indexer.run(store=False)
        result = indexer.index()
        eq_(len(result), 2)
