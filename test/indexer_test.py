from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.fs.explorer import FilterMismatchException, FilterNotFoundException
from duplicates.indexer import Indexer
from duplicates.libraries.utils import epoch, serialize_date
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
        indexer.run(persist=False)
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

    def test_last_update(self):
        index = Indexer(TEST_DIR, unix_patterns=['*.jpg', '*.test'])
        index = index.index()
        assert index.last_update != serialize_date(epoch)

    def test_timestamp_update_only_if_index_is_updated(self):
        indexer = Indexer(TEST_DIR, unix_patterns=['*.jpg', '*.test'])
        update_time = indexer.index().last_update
        not_updated = indexer.index().last_update
        assert update_time == not_updated, "%r != %r" % (update_time, not_updated)

    def test_store(self):
        self.indexer.run()
        assert_true(os.path.isfile(STORE_PATH))
