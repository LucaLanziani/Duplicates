from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.data_store import FILESTORE
from duplicates.main import Duplicates
from nose.tools import eq_, ok_

TEST_DIR = './test/files/'


class DuplicatesTest(unittest.TestCase):

    def setUp(self):
        self.duplicates = Duplicates(TEST_DIR)

    def test_collect_data(self):
        result = self.duplicates.collect_data()
        eq_(len(result), 3)

    def test_run_no_store(self):
        self.duplicates.run(store=False)
        ok_(not os.path.isfile(self.duplicates.store_path), "%s should not exist" % FILESTORE)

    def test_run_with_store(self):
        self.duplicates.run()
        ok_(os.path.isfile(self.duplicates.store_path), "something went wrong saving the data")
        os.remove(self.duplicates.store_path)

    def test_empty_unix_patters(self):
        duplicates = Duplicates(TEST_DIR, unix_patterns=[])
        result = duplicates.collect_data()
        eq_(len(result), 3)

    def test_asterisk_unix_pattern(self):
        duplicates = Duplicates(TEST_DIR, unix_patterns="*")
        result = duplicates.collect_data()
        eq_(len(result), 3)
