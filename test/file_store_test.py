from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import unittest

from data_store import FileStore, FILESTORE
from file_attr import FileAttr
from nose.tools import eq_

from utils import epoch, deserialize_date

TEST_DIR = './test/files/'
TEST_FILE = './test/files/empty file.exe.test'
FILE_STORE_PATH = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)

STORE_CONTENT = (
 'H4sICCQgsFQC/y5kdXBsaWNhdGVzLmpzb24ArVHJboMwEL3nKxDnho63MOY7emoVIQePBWogqHbV'
 'JeLfa5yC0kXqpT6NZt424/Mmiy9/HE4vQz2a0A6mJ59X2UMapKHYOeOIOeVgVyrdSIkCJAJTTJXY'
 'oFAojGu0cOXBKpJI0ukItppJUzqeJ6n9TXbxWl1qE8JTtDr/o9W1WlI89qHrKfaZ5IAcQarPICtk'
 'CRRBeXFL/RjeMtcdqaBXKgL5kH9ntMa3M9pKZrGxGh3AgYMkjQBaIzUOJS/pB9F377MNrN0pVdNy'
 'm+fRmkB21uZx6S2wLeg7hpXAimOByECo+0U25ajDqZ7T+q+X/DPa9Rcnxu+rr5j9Jelm+gCc8H0m'
 'MwIAAA==')  # noqa
STORE_LAST_UPDATE = '2015-01-09T18:38:28.881035Z'


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

    def remove_pathane_test(self):
        self.add_pathname_test()
        self.store.remove_pathname(TEST_FILE)
        eq_(False, self.store.is_file_known(self.file_attr))

    def save_test(self):
        self.store.add_file(self.file_attr)
        self.store.save()
        assert os.path.isfile(self.store.store_path)

    def _write_store(self):
        with open(FILE_STORE_PATH, 'wb') as fp:
            fp.write(STORE_CONTENT.decode('base64'))

    def load_test(self):
        self._write_store()
        self.store.load()
        eq_(True, self.store.is_file_known(self.file_attr))

    def last_update_test(self):
        eq_(self.store.last_update, epoch)
        self._write_store()
        self.store.load()
        eq_(self.store.last_update, deserialize_date(STORE_LAST_UPDATE))
