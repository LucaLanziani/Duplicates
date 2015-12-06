from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from duplicates.gatherer import Gatherer
from nose.tools import eq_

TEST_DIR = './test/files/'


class DuplicatesTest(unittest.TestCase):

    def setUp(self):
        self.duplicates = Gatherer(TEST_DIR)

    def test_collect_data(self):
        result = self.duplicates.collect_data()
        eq_(len(result), 3)

    def test_empty_unix_patters(self):
        duplicates = Gatherer(TEST_DIR, unix_patterns=[])
        result = duplicates.collect_data()
        eq_(len(result), 3)

    def test_asterisk_unix_pattern(self):
        duplicates = Gatherer(TEST_DIR, unix_patterns="*")
        result = duplicates.collect_data()
        eq_(len(result), 3)
