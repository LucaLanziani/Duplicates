# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from duplicates.fs.file_attr import FileAttr, FileNotFoundError
from nose.tools import eq_, ok_, raises

TEST_FILE = './test/files/test_dir_1/empty file.exe.test'
MD5 = 'd41d8cd98f00b204e9800998ecf8427e'
SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

UNICODE_PATHNAME = './test/files/test_dir_1/03_Руководство_по_эксплуатации.jpg'


class FileAttrTest(unittest.TestCase):

    def tearDown(self):
        pass

    @raises(FileNotFoundError)
    def test_raise_if_file_not_exist(self):
        FileAttr.get('./notExists', TEST_FILE.replace('test', 'notExists'))

    def test_md5(self):
        eq_(FileAttr._md5(TEST_FILE), MD5)

    def test_sha1(self):
        eq_(FileAttr._sha1(TEST_FILE), SHA1)

    def test_sha256(self):
        eq_(FileAttr._sha256(TEST_FILE), SHA256)

    def test_hash(self):
        eq_(FileAttr._hash(TEST_FILE), MD5)

    def test_size(self):
        eq_(FileAttr._size(TEST_FILE), 0)

    def test_directory(self):
        ok_(os.path.isdir(FileAttr._directory(TEST_FILE)))

    def test_filename(self):
        eq_(FileAttr._filename(TEST_FILE), 'empty file.exe.test')

    def test_extention(self):
        eq_(FileAttr._extension(TEST_FILE), '.test')

    def test_unicode_filename(self):
        ph = FileAttr._pathname_hash(UNICODE_PATHNAME)
        eq_(ph, '9e99520ee361ddcf651ae1d715cda6166ac65fb8d78f93101f19264dd1fcbd7c')
