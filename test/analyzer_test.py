from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.indexer import Indexer
from nose.tools import eq_

TEST_DIR = './test/files/'

class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        Indexer(TEST_DIR).index()
        self._test_dir = open(TEST_DIR, "r")
        self._test_dir.