from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.fs.explorer import Explorer
from nose.tools import eq_

TEST_DIR = os.path.join(os.path.dirname(__file__), 'files/test_dir_1/')


class IndexerTest(unittest.TestCase):

    def setUp(self):
        self.explorer = Explorer(TEST_DIR)

    def test_list_length(self):
        result = self.explorer.list()
        eq_(len(list(result)), 3)
