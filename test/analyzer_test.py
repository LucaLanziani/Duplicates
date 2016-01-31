from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.analyzer import Analyzer
from duplicates.indexer import Indexer
from duplicates.store.inmemory_store import InmemoryStore
from nose.tools import eq_

TEST_DIR_1 = './test/files/test_dir_1'
TEST_DIR_2 = './test/files/test_dir_2'


class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.first_store = Indexer(TEST_DIR_1, store=InmemoryStore).index()
        self.second_store = Indexer(TEST_DIR_2, store=InmemoryStore).index()
        self.analyzer = Analyzer()

    def test_duplicates(self):
        duplicates = list(self.analyzer.duplicates(self.first_store))
        eq_(len(duplicates), 1)

    def test_intersection(self):
        intersection = self.analyzer.intersection(self.first_store, self.second_store)
        print(intersection)
        eq_(len(intersection), 2)

    def test_difference(self):
        difference = self.analyzer.difference(self.second_store, self.first_store)
        print(difference)
        eq_(len(difference), 1)
