from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from file_attr import FileAttr, FileNotFoundError
from nose.tools import raises

TEST_FILE = './test/empty_file.test'
MD5 = 'd41d8cd98f00b204e9800998ecf8427e'
SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


class FileAttrTest(unittest.TestCase):

    def setUp(self):
        self.file_attr = FileAttr(TEST_FILE)

    @raises(FileNotFoundError)
    def raise_if_file_not_exist_test(self):
        FileAttr(TEST_FILE.replace('test', 'notExists'))
