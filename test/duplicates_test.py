from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from nose.tools import eq_

from duplicates.main import Duplicates

TEST_DIR = './test/files/'


class DuplicatesTest(unittest.TestCase):

    def setUp(self):
        self.duplicates = Duplicates(TEST_DIR)

    def test_collect_data(self):
        result = self.duplicates.collect_data()
        eq_(len(result), 2)
