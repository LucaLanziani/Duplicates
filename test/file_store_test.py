from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import unittest

from data_store import FileStore, FILESTORE
from file_attr import FileAttr
from nose.tools import eq_

TEST_DIR = './test'
TEST_FILE = './test/empty file.exe.test'
FILE_STORE_PATH = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)
STORE_CONTENT = ('H4sICFhjrFQC/y5kdXBsaWNhdGVzLmpzb24ArZFNbsMgEIX3OYXFukoHDB7o'
                 'VarI4meQrcZOFJCi\nNPLda5PGSptFN2WF5r153zBcN9V82Md4OI/t0eZutA'
                 'Ml9la9F6GI6BHRO86Dd6aOFB26mngw6DwE\nJxpbeycwEnjAhigalNIr5RUq'
                 'q+uGlajdS3VjrZTW5nyaUdd/RD2mlcT9kPuB5jqXApTmyojvQVbL\nfaDZxL'
                 'avNBzzpY39nraZUma/3Z1N3eIMkgftg9ERwAmQZDSAMZp81FIgPTWm/nNBwF'
                 'qdym2672UJ\nbvOhoNPPtfzJevyv0vH8jlXf3bCb6QtNxfd8/AEAAA==\n')


class FileStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = FileStore({'DIRECTORY': TEST_DIR})
        self.file_attr = FileAttr(TEST_FILE)

    def tearDown(self):
        try:
            os.remove(FILE_STORE_PATH)
        except OSError:
            pass

    def have_the_cwd_as_base_dir_test(self):
        eq_(self.store.base_dir, os.path.dirname(__file__))

    def store_path_will_be_in_cwd_test(self):
        print(os.path.abspath(TEST_DIR))
        expected_path = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)
        eq_(expected_path, self.store.store_path)

    def add_pathname_test(self):
        self.store.add_file(self.file_attr)
        eq_(True, self.store.is_file_known(self.file_attr))

    def remove_pathane_test(self):
        self.add_pathname_test()
        self.store.remove_pathname(TEST_FILE)
        eq_(False, self.store.is_file_known(self.file_attr))

    def save_test(self):
        self.store.add_file(self.file_attr)
        self.store.save()
        assert os.path.isfile(self.store.store_path)

    def load_test(self):
        with open(FILE_STORE_PATH, 'wb') as fp:
            fp.write(STORE_CONTENT.decode('base64'))
        self.store.load()
        eq_(True, self.store.is_file_known(self.file_attr))
