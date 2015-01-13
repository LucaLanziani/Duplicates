# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.data_store import FileStore, FILESTORE
from duplicates.file_attr import FileAttr
from duplicates.utils import absolute_path
from nose.tools import eq_

TEST_DIR = './test/files/'
TEST_FILE = './test/files/empty file.exe.test'
FILE_STORE_PATH = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)


class FileStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = FileStore(TEST_DIR)
        self.file_attr = FileAttr(TEST_FILE)

    def tearDown(self):
        try:
            os.remove(FILE_STORE_PATH)
        except OSError:
            pass

    def store_path_will_be_in_cwd_test(self):
        expected_path = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)
        eq_(expected_path, self.store.store_path)

    def add_pathname_test(self):
        self.store.add_file(self.file_attr)
        eq_(True, self.store.is_file_known(self.file_attr))

    def remove_pathnane_test(self):
        self.add_pathname_test()
        self.store.remove_pathname(absolute_path(TEST_FILE))
        eq_(False, self.store.is_file_known(self.file_attr))

    def save_test(self):
        self.store.add_file(self.file_attr)
        self.store.save()
        eq_(True, os.path.isfile(self.store.store_path))

    def load_test(self):
        self.store.add_file(self.file_attr)
        self.store.save()
        store = FileStore(TEST_DIR)
        eq_(True, store.is_file_known(self.file_attr))

    def unknow_file_test(self):
        eq_(False, self.store.is_file_known(self.file_attr))

    def different_lmtime_file_test(self):
        self.store.add_file(self.file_attr)
        os.utime(TEST_FILE, None)
        eq_(False, self.store.is_file_known(self.file_attr))
