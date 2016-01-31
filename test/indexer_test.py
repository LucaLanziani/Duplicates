from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest
import os

from duplicates.indexer import Indexer
from duplicates.store.json_store import FILESTORE
from nose.tools import eq_, assert_true

TEST_DIR = './test/files/test_dir_1/'
STORE_PATH = os.path.join(TEST_DIR, FILESTORE)

class IndexerTest(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer(TEST_DIR)

    def tearDown(self):
        if os.path.isfile(STORE_PATH):
            os.unlink(STORE_PATH)

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

    def test_store(self):
        self.indexer.run()
        assert_true(os.path.isfile(STORE_PATH))
