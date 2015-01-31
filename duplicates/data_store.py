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

FILESTORE = ".duplicates.json.gz"
KNOWN_PATHNAMES_HASHES = 'known_pathnames_hashes'
PATHNAME_HASH_TO_ATTRS = 'pathname_hash_to_attrs'
FILE_HASH_TO_PATHNAMES = 'file_hash_to_pathnames'

SIZE = 'size'
LMTIME = 'lmtime'
HASH = 'hash'
PATHNAME = 'pathname'
LAST_UPDATE = 'updated'


class FileStore(object):

    """Store information about duplicates

    The data are kept in a gziped json file inside the analized directory,
    all the pathnames in the filestore are "local", by "local" we intend a
    relative pathname from the filestore location.

    The store contains three main structures:

        KNOWN_PATHNAMES_HASHES:
            A list containing all the hashes of the known pathnames

        PATHNAME_HASH_TO_ATTRS:
            a dictionary with pathname_hash as key and file attributes
            (SIZE, LMTIME, HASH, PATHNAME) as value

        FILE_HASH_TO_PATHNAMES:
            a dictionary that has the file hash as key and a list of pathnames,
            of the files that generate that hash, as value

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
                KNOWN_PATHNAMES_HASHES: [],
                PATHNAME_HASH_TO_ATTRS: {},
                FILE_HASH_TO_PATHNAMES: {},
                LAST_UPDATE: serialize_date(epoch)
            }

    def _to_json(self, data):
        with gzip.open(self.store_path, 'wb') as fd:
            json.dump(data, fd, indent=4)

    def _local_path(self, abs_pathname):
        return abs_pathname.replace(self._base_dir, '.')

    def _local_data(self, file_attr):
        local_pathname = self._local_path(file_attr.pathname)
        local_pathname_hash = FileAttr.hash_pathname(local_pathname)
        return local_pathname, local_pathname_hash

    def _add_file(self, file_attr):
        local_pathname, local_pathname_hash = self._local_data(file_attr)
        self.hash_to_pathnames[file_attr.hash].append(local_pathname)
        self.pathname_hash_to_attr[local_pathname_hash] = {
            SIZE: file_attr.size,
            LMTIME: file_attr.lmtime,
            HASH: file_attr.hash,
            PATHNAME: local_pathname
        }
        self.known_pathnames_hashes.add(local_pathname_hash)

    def _rename_key(self, dictionary, old, new):
        if old in dictionary and old != new:
            dictionary[new] = dictionary[old]
            del dictionary[old]

    def _convert_old_data_format(self, data):
        conversions = [
            ('known_pathnames', KNOWN_PATHNAMES_HASHES),
            ('pathnames_attr', PATHNAME_HASH_TO_ATTRS),
            ('hash_to_files', FILE_HASH_TO_PATHNAMES)
        ]
        for conversion in conversions:
            self._rename_key(data, *conversion)
        return data

    def _absolute_pathname(self, local_pathname):
        return os.path.normpath(os.path.join(self._base_dir, local_pathname))

    def add_file(self, file_attr):
        if not self.is_file_known(file_attr):
            self._add_file(file_attr)

    def is_file_known(self, file_attr):
        local_pathname, local_pathname_hash = self._local_data(file_attr)
        if local_pathname_hash not in self.known_pathnames_hashes:
            return False
        else:
            stored_attr = self.pathname_hash_to_attr[local_pathname_hash]
            diff_size = stored_attr[SIZE] != file_attr.size
            diff_time = stored_attr[LMTIME] != file_attr.lmtime
            if diff_size or diff_time:
                return False
            return True

    @property
    def known_pathnames_hashes(self):
        return self._data[KNOWN_PATHNAMES_HASHES]

    @property
    def pathname_hash_to_attr(self):
        return self._data[PATHNAME_HASH_TO_ATTRS]

    @property
    def hash_to_pathnames(self):
        return self._data[FILE_HASH_TO_PATHNAMES]

    @property
    def last_update(self):
        return self._data[LAST_UPDATE]

    def load(self):
        data = self._from_json()
        data = self._convert_old_data_format(data)
        current_data = data[FILE_HASH_TO_PATHNAMES]
        data[FILE_HASH_TO_PATHNAMES] = defaultdict(list, current_data)
        data[KNOWN_PATHNAMES_HASHES] = set(data[KNOWN_PATHNAMES_HASHES])
        if LAST_UPDATE not in data:
            data[LAST_UPDATE] = serialize_date(epoch)
        data[LAST_UPDATE] = deserialize_date(data[LAST_UPDATE])
        self._data = data

    def save(self):
        self._data[LAST_UPDATE] = datetime.utcnow()
        data = self._data.copy()
        data[KNOWN_PATHNAMES_HASHES] = list(data[KNOWN_PATHNAMES_HASHES])
        data[LAST_UPDATE] = serialize_date(data[LAST_UPDATE])
        self._to_json(data)

    def _remove_pathname(self, local_pathname):
        local_pathname_hash = FileAttr.hash_pathname(local_pathname)
        self.known_pathnames_hashes.remove(local_pathname_hash)
        stored_data = self.pathname_hash_to_attr[local_pathname_hash]
        self.hash_to_pathnames[stored_data[HASH]].remove(stored_data[PATHNAME])
        del(self.pathname_hash_to_attr[local_pathname_hash])

    def remove_pathname(self, abs_pathname):
        assert(os.path.isabs(abs_pathname))
        local_pathname = self._local_path(abs_pathname)
        self._remove_pathname(local_pathname)

    def duplicates(self):
        for _, paths in self.hash_to_pathnames.iteritems():
            if len(paths) > 1:
                yield map(lambda path: self._absolute_pathname(path), paths)

    def __repr__(self):
        return repr(self._data)

    def __len__(self):
        return len(self._data[KNOWN_PATHNAMES_HASHES])
