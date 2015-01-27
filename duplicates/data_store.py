# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import gzip
import json
import os
from collections import defaultdict
from datetime import datetime

from duplicates.file_attr import FileAttr
from duplicates.utils import (absolute_path, deserialize_date, epoch,
                              serialize_date)

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
    """store information about duplicates

    The data are kept in a gziped json file inside the analized directory,
    all the pathnames in the filestore are "local", by "local" we intend a
    relative pathname from the filestore location.
    """

    def __init__(self, filepath):
        super(FileStore, self).__init__()
        self.store_path = absolute_path(filepath)
        if os.path.isdir(self.store_path):
            self.store_path = os.path.join(self.store_path, FILESTORE)
        self._base_dir = os.path.dirname(self.store_path)
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
                LAST_UPDATE: serialize_date(epoch)
            }

    def _to_json(self):
        with gzip.open(self.store_path, 'wb') as fd:
            json.dump(self._data, fd, indent=4)

    def _local_path(self, abs_pathname):
        return abs_pathname.replace(self._base_dir, '.')

    def _local_data(self, file_attr):
        local_pathname = self._local_path(file_attr.pathname)
        local_pathname_hash = FileAttr.hash_pathname(local_pathname)
        return local_pathname, local_pathname_hash

    def _add_file(self, file_attr):
        local_pathname, local_pathname_hash = self._local_data(file_attr)
        self.hash_to_files[file_attr.hash].append(local_pathname)
        self.pathnames_attr[local_pathname_hash] = {
            SIZE: file_attr.size,
            LMTIME: file_attr.lmtime,
            HASH: file_attr.hash,
            PATHNAME: local_pathname
        }
        self.known_pathnames.add(local_pathname_hash)

    def add_file(self, file_attr):
        if not self.is_file_known(file_attr):
            self._add_file(file_attr)

    def is_file_known(self, file_attr):
        local_pathname, local_pathname_hash = self._local_data(file_attr)
        if local_pathname_hash not in self.known_pathnames:
            return False
        else:
            stored_attr = self.pathnames_attr[local_pathname_hash]
            diff_size = stored_attr[SIZE] != file_attr.size
            diff_time = stored_attr[LMTIME] != file_attr.lmtime
            if diff_size or diff_time:
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

    @property
    def last_update(self):
        return self._data[LAST_UPDATE]

    def load(self):
        data = self._from_json()
        data[HASH_TO_FILES] = defaultdict(list, data[HASH_TO_FILES])
        data[KNOWN_PATHNAMES] = set(data[KNOWN_PATHNAMES])
        if LAST_UPDATE not in data:
            data[LAST_UPDATE] = serialize_date(epoch)
        data[LAST_UPDATE] = deserialize_date(data[LAST_UPDATE])
        self._data = data

    def save(self):
        self._data[KNOWN_PATHNAMES] = list(self.known_pathnames)
        self._data[LAST_UPDATE] = serialize_date(datetime.utcnow())
        self._to_json()

    def _remove_pathname(self, local_pathname):
        local_pathname_hash = FileAttr.hash_pathname(local_pathname)
        self.known_pathnames.remove(local_pathname_hash)
        stored_data = self.pathnames_attr[local_pathname_hash]
        self.hash_to_files[stored_data[HASH]].remove(stored_data[PATHNAME])
        del(self.pathnames_attr[local_pathname_hash])

    def remove_pathname(self, abs_pathname):
        assert(os.path.isabs(abs_pathname))
        local_pathname = self._local_path(abs_pathname)
        self._remove_pathname(local_pathname)

    def duplicates(self):
        for _, paths in self.hash_to_files.iteritems():
            if len(paths) > 1:
                yield map(lambda path: absolute_path(path), paths)

    def __repr__(self):
        return repr(self._data)
