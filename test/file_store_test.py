# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest
from datetime import datetime, timedelta

from duplicates.data_store import FileStore, FILESTORE
from duplicates.file_attr import FileAttr
from duplicates.utils import absolute_path
from nose.tools import eq_, ok_

TEST_DIR = './test/files/'
TEST_FILE = '%sempty file.exe.test' % TEST_DIR
UNICODE_PATHNAME = '%s03_Руководство_по_эксплуатации.jpg' % TEST_DIR
BIGGER_FILE = '%stestfile_10MB' % TEST_DIR

FILESTORE_PATH = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)


class FileStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = FileStore(TEST_DIR)
        self.file_attr = FileAttr(TEST_FILE)

    def tearDown(self):
        try:
            os.remove(FILESTORE_PATH)
        except OSError:
            pass

    def _add_file_and_save(self, filestore):
        filestore.add_file(self.file_attr)
        filestore.save()

    def test_store_path_will_be_in_cwd(self):
        expected_path = os.path.join(os.path.abspath(TEST_DIR), FILESTORE)
        eq_(expected_path, self.store.store_path)

    def test_add_pathname(self):
        self.store.add_file(self.file_attr)
        eq_(True, self.store.is_file_known(self.file_attr))

    def test_remove_pathname(self):
        self.test_add_pathname()
        self.store.remove_pathname(absolute_path(TEST_FILE))
        eq_(False, self.store.is_file_known(self.file_attr))

    def test_save(self):
        self._add_file_and_save(self.store)
        eq_(True, os.path.isfile(self.store.store_path))

    def test_load(self):
        self._add_file_and_save(self.store)
        store = FileStore(TEST_DIR)
        eq_(True, store.is_file_known(self.file_attr))

    def test_unknow_file(self):
        eq_(False, self.store.is_file_known(self.file_attr))

    def test_different_lmtime_file(self):

        self.store.add_file(self.file_attr)
        os.utime(TEST_FILE, None)
        eq_(False, self.store.is_file_known(self.file_attr))

    def test_using_filepath(self):
        store = FileStore(FILESTORE_PATH)
        self._add_file_and_save(store)
        eq_(True, os.path.isfile(FILESTORE_PATH))

    def test_load_old_data_version(self):
        def from_json():
            return {
                'known_pathnames': [],
                'pathnames_attr': {},
                'hash_to_files': {}
            }

        def to_json(data):
            assert 'known_pathnames_hashes' in data
            assert 'file_hash_to_pathnames' in data
            assert 'pathname_hash_to_attrs' in data

        self.store._from_json = from_json
        self.store._to_json = to_json
        self.store.load()
        self.store.save()

    def test_duplicates(self):
        empty_file = FileAttr(TEST_FILE)
        unicode_file = FileAttr(UNICODE_PATHNAME)
        self.store.add_file(empty_file)
        self.store.add_file(unicode_file)
        self.store.add_file(FileAttr(BIGGER_FILE))
        eq_(list(self.store.duplicates()), [
            [empty_file.pathname, unicode_file.pathname]
        ])

    def test_last_update(self):
        def to_json(data):
            pass

        eq_(self.store.last_update, datetime(1970, 1, 1))
        self.store.add_file(self.file_attr)
        self.store._to_json = to_json
        self.store.save()
        ok_(datetime.utcnow() - self.store.last_update < timedelta(seconds=1))
