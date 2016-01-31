from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.indexer import Indexer
from duplicates.analyzer import Analyzer
from nose.tools import eq_

TEST_DIR_1 = './test/files/test_dir_1'
TEST_DIR_2 = './test/files/test_dir_2'

class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.first_store = Indexer(TEST_DIR_1).index()
        self.second_store = Indexer(TEST_DIR_2).index()
        self.analyzer = Analyzer()

    def test_duplicates(self):
        duplicates = list(self.analyzer.duplicates(self.second_store))
        eq_(len(duplicates), 1)

    def test_intersection(self):
        # TODO
        pass
