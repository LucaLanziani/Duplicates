# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from file_attr import FileAttr, FileNotFoundError, FileAttrFactory
from nose.tools import raises, eq_

TEST_FILE = './test/files/empty file.exe.test'
MD5 = 'd41d8cd98f00b204e9800998ecf8427e'
SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


class FileAttrTest(unittest.TestCase):

    def setUp(self):
        self.file_attr = FileAttr(TEST_FILE)

    def tearDown(self):
        pass

    @raises(FileNotFoundError)
    def raise_if_file_not_exist_test(self):
        FileAttr(TEST_FILE.replace('test', 'notExists'))

    def md5_test(self):
        eq_(self.file_attr.md5, MD5)

    def sha1_test(self):
        eq_(self.file_attr.sha1, SHA1)

    def sha256_test(self):
        eq_(self.file_attr.sha256, SHA256)

    def hash_test(self):
        eq_(self.file_attr.hash, MD5)

    def size_test(self):
        eq_(self.file_attr.size, 0)

    def extention_test(self):
        eq_(self.file_attr.extention, '.test')

    def similarity_test(self):
        eq_(self.file_attr.similar(self.file_attr), True)


class FileAttrFactoryTest(unittest.TestCase):

    def by_pathname_test(self):
        first = FileAttrFactory.by_pathname(TEST_FILE)
        second = FileAttrFactory.by_pathname(TEST_FILE)
        eq_(first, second)
