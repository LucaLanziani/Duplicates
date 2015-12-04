# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from duplicates.fs.file_attr import FileAttr
from duplicates.store.dummy_store import DummyStore
from duplicates.utils import (epoch, serialize_date)

FILESTORE = ".duplicates.json.gz"
KNOWN_PATHNAMES_HASHES = 'known_pathnames_hashes'
PATHNAME_HASH_TO_ATTRS = 'pathname_hash_to_attrs'
FILE_HASH_TO_PATHNAMES = 'file_hash_to_pathnames'

SIZE = 'size'
LMTIME = 'lmtime'
HASH = 'hash'
PATHNAME = 'pathname'
LAST_UPDATE = 'updated'


class InmemoryStore(DummyStore):

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

    def __init__(self):
        default_data = {
            KNOWN_PATHNAMES_HASHES: set([]),
            PATHNAME_HASH_TO_ATTRS: {},
            FILE_HASH_TO_PATHNAMES: {},
            LAST_UPDATE: serialize_date(epoch)
        }
        self.store_path = None
        super(InmemoryStore, self).__init__(default_data)
        self.load()

    def _local_path(self, abs_pathname):
        return abs_pathname.replace(self._base_dir, '.')

    def _absolute_pathname(self, local_pathname):
        return os.path.normpath(os.path.join(self._base_dir, local_pathname))

    def _add_file(self, file_attr):
        pathname = file_attr.pathname
        pathname_hash = FileAttr.hash_pathname(pathname)
        if file_attr.hash not in self._hash_to_pathnames:
            self._hash_to_pathnames[file_attr.hash] = []
        self._hash_to_pathnames[file_attr.hash].append(pathname)
        self._pathname_hash_to_attr[pathname_hash] = {
            SIZE: file_attr.size,
            LMTIME: file_attr.lmtime,
            HASH: file_attr.hash,
            PATHNAME: pathname
        }
        self._known_pathnames_hashes.add(pathname_hash)

    def _remove_pathname(self, pathname):
        pathname_hash = FileAttr.hash_pathname(pathname)

        self._known_pathnames_hashes.remove(pathname_hash)
        stored_data = self._pathname_hash_to_attr[pathname_hash]
        self._hash_to_pathnames[stored_data[HASH]].remove(stored_data[PATHNAME])
        del(self._pathname_hash_to_attr[pathname_hash])

    def add_file(self, file_attr):
        if not self.is_file_known(file_attr):
            self._add_file(file_attr)

    def is_file_known(self, file_attr):
        pathname = file_attr.pathname
        pathname_hash = FileAttr.hash_pathname(pathname)
        if pathname_hash not in self._known_pathnames_hashes:
            return False
        else:
            stored_attr = self._pathname_hash_to_attr[pathname_hash]
            diff_size = stored_attr[SIZE] != file_attr.size
            diff_time = stored_attr[LMTIME] != file_attr.lmtime
            if diff_size or diff_time:
                return False
            return True

    def remove_pathname(self, pathname):
        self._remove_pathname(pathname)

    def paths_by_hash(self):
        for hash, paths in self._hash_to_pathnames.iteritems():
            yield hash, paths

    def __repr__(self):
        return repr(self._data)

    def __len__(self):
        return len(self._known_pathnames_hashes)

    @property
    def _known_pathnames_hashes(self):
        return self._data[KNOWN_PATHNAMES_HASHES]

    @property
    def _pathname_hash_to_attr(self):
        return self._data[PATHNAME_HASH_TO_ATTRS]

    @property
    def _hash_to_pathnames(self):
        return self._data[FILE_HASH_TO_PATHNAMES]

    @property
    def _last_update(self):
        return self._data[LAST_UPDATE]
