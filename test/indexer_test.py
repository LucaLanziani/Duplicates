from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.fs.explorer import FilterMismatchException, FilterNotFoundException
from duplicates.indexer import Indexer
from duplicates.store.json_store import FILESTORE
from nose.tools import assert_true, eq_, raises


TEST_DIR = os.path.join(os.path.dirname(__file__), 'files/test_dir_1/')

STORE_PATH = os.path.join(TEST_DIR, FILESTORE)


class IndexerTest(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer(TEST_DIR, unix_patterns="*")

    def tearDown(self):
        if os.path.isfile(STORE_PATH):
            os.unlink(STORE_PATH)

    def test_collect_data(self):
        result = self.indexer.index()
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

    @raises(FilterNotFoundException)
    def test_with_no_filter(self):
        Indexer(TEST_DIR)

    @raises(FilterMismatchException)
    def test_existing_filter(self):
        indexer = Indexer(TEST_DIR, unix_patterns=['*.jpg'])
        indexer.run()
        indexer = Indexer(TEST_DIR, unix_patterns=['*.jpg', '*.test'])
        indexer.run()

    def test_store(self):
        self.indexer.run()
        assert_true(os.path.isfile(STORE_PATH))
