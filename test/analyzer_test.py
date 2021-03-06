from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.analyzer import Analyzer
from duplicates.indexer import Indexer
from duplicates.store.inmemory_store import InmemoryStore
from nose.tools import eq_

TEST_DIR_1 = os.path.join(os.path.dirname(__file__), 'files/test_dir_1/')
TEST_DIR_2 = os.path.join(os.path.dirname(__file__), 'files/test_dir_2/')


class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.first_index = Indexer(TEST_DIR_1, unix_patterns="*", storeCLS=InmemoryStore).index()
        self.second_index = Indexer(TEST_DIR_2, unix_patterns="*", storeCLS=InmemoryStore).index()
        self.analyzer = Analyzer()

    def test_duplicates(self):
        duplicates = list(self.analyzer.duplicates(self.first_index))
        eq_(len(duplicates), 1)

    def test_intersection(self):
        intersection = self.analyzer.intersection(self.first_index, self.second_index)
        eq_(len(intersection), 2)

    def test_difference(self):
        difference = self.analyzer.difference(self.first_index, self.second_index)
        eq_(len(difference), 1)
