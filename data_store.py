from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import gzip
import json
import os
from collections import defaultdict

from file_attr import FileAttr
from utils import absolute_path

FILESTORE = ".duplicates.json"
FILESTORE = ".duplicates.json.gz"
KNOWN_PATHNAMES = 'known_pathnames'
PATHNAMES_ATTR = 'pathnames_attr'
HASH_TO_FILES = 'hash_to_files'

SIZE = 'size'
LMTIME = 'lmtime'
HASH = 'hash'
PATHNAME = 'pathname'
LAST_UPDATE = 'updated'


class FileStore(object):
    """store information about duplicates"""
    def __init__(self, directory):
        super(FileStore, self).__init__()
        self.base_dir = absolute_path(directory)
        self.store_path = os.path.join(self.base_dir, FILESTORE)
        self.load()

    def _from_json(self):
        try:
            with gzip.open(self.store_path, 'rb') as fd:
                result = json.load(fd)

            return result
        except Exception:
            return {
                KNOWN_PATHNAMES: [],
                PATHNAMES_ATTR: {},
                HASH_TO_FILES: {},
            }

    def _to_json(self):
        with gzip.open(self.store_path, 'wb') as fd:
            json.dump(self._data, fd, indent=4)

    def _rel_path(self, pathname):
        if not os.path.isabs(pathname):
            pathname = absolute_path(pathname)
        return pathname.replace(self.base_dir, '.')

    def _relative_data(self, file_attr):
        rel_pathname = self._rel_path(file_attr.pathname)
        rel_pathname_hash = FileAttr.hash_pathname(rel_pathname)
        return rel_pathname, rel_pathname_hash

    def _add_file(self, file_attr):
        rel_pathname, rel_pathname_hash = self._relative_data(file_attr)
        self.hash_to_files[file_attr.hash].append(rel_pathname)
        self.pathnames_attr[rel_pathname_hash] = {
            SIZE: file_attr.size,
            LMTIME: file_attr.lmtime,
            HASH: file_attr.hash,
            PATHNAME: rel_pathname
        }
        self.known_pathnames.add(rel_pathname_hash)

    def add_file(self, file_attr):
        rel_pathname, _ = self._relative_data(file_attr)
        if not self.is_file_known(file_attr):
            self._add_file(file_attr)

    def is_file_known(self, file_attr):
        rel_pathname, pathname_hash = self._relative_data(file_attr)
        if pathname_hash not in self.known_pathnames:
            return False
        else:
            stored_attr = self.pathnames_attr[pathname_hash]
            diff_size = stored_attr[SIZE] != file_attr.size
            diff_time = stored_attr[LMTIME] != file_attr.lmtime
            if diff_size or diff_time:
                self.remove_pathname(rel_pathname)
                return False
            return True

    @property
    def known_pathnames(self):
        return self._data[KNOWN_PATHNAMES]

    @property
    def pathnames_attr(self):
        return self._data[PATHNAMES_ATTR]

    @property
    def hash_to_files(self):
        return self._data[HASH_TO_FILES]

    def load(self):
        data = self._from_json()
        data[HASH_TO_FILES] = defaultdict(list, data[HASH_TO_FILES])
        data[KNOWN_PATHNAMES] = set(data[KNOWN_PATHNAMES])
        self._data = data

    def save(self):
        self._data[KNOWN_PATHNAMES] = list(self.known_pathnames)
        self._to_json()

    def remove_pathname(self, pathname):
        rel_pathname_hash = FileAttr.hash_pathname(self._rel_path(pathname))
        self.known_pathnames.remove(rel_pathname_hash)
        stored_data = self.pathnames_attr[rel_pathname_hash]
        self.hash_to_files[stored_data['hash']].remove(stored_data['pathname'])
        del(self.pathnames_attr[rel_pathname_hash])

    def duplicates(self):
        for _, paths in self.hash_to_files.iteritems():
            if len(paths) > 1:
                yield map(lambda path: absolute_path(path), paths)

    def __repr__(self):
        return repr(self._data)
