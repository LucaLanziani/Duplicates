from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from data_store import FileStore, FILESTORE
from file_attr import FileAttr

TEST_DIR = './test'
TEST_FILE = './test/empty_file.test'
MD5 = 'd41d8cd98f00b204e9800998ecf8427e',
SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


class FileStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = FileStore({'DIRECTORY': TEST_DIR})
        self.file_attr = FileAttr(TEST_FILE)

    def tearDown(self):
        try:
            os.remove(os.path.join(os.path.abspath(TEST_DIR), FILESTORE))
        except OSError:
            pass

    def have_the_cwd_as_base_dir_test(self):
        assert self.store.base_dir == os.path.dirname(__file__)

    def store_path_will_be_in_cwd_test(self):
        print(os.path.abspath(TEST_DIR))
        expected_path = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)
        assert expected_path == self.store.store_path

    def add_pathname_test(self):
        self.store.add_file(self.file_attr)
        assert True == self.store.is_file_known(self.file_attr)

    def remove_pathane_test(self):
        self.add_pathname_test()
        self.store.remove_pathname(TEST_FILE)
        assert False == self.store.is_file_known(self.file_attr)

    def save_test(self):
        self.store.add_file(self.file_attr)
        self.store.save()
        assert os.path.isfile(self.store.store_path)

    def load_test(self):
        pass
