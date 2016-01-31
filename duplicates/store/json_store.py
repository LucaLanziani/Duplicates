# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import gzip
import json
import logging
import os

from collections import defaultdict

from duplicates.libraries.utils import absolute_path, DuplicateExceptions
from duplicates.store.inmemory_store import FILE_HASH_TO_PATHNAMES, InmemoryStore, KNOWN_PATHNAMES_HASHES

FILESTORE = ".duplicates.json.gz"

log = logging.getLogger(__name__)


class StoreNotFoundError(DuplicateExceptions):
    pass


class JsonStore(InmemoryStore):

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

    def __init__(self, directory):
        self._directory = absolute_path(directory)
        self.store_path = os.path.join(self._directory, FILESTORE)
        super(JsonStore, self).__init__(directory)

    def _from_json(self):
        try:
            with gzip.open(self.store_path, 'rb') as fd:
                result = json.load(fd)
            return result
        except Exception as e:
            log.exception('Something went wrong trying to load the store from %s', self.store_path)
            raise e

    def _to_json(self):
        try:
            self._data[KNOWN_PATHNAMES_HASHES] = list(self._known_pathnames_hashes)
            with gzip.open(self.store_path, 'wb') as fd:
                json.dump(self._data, fd, indent=4)
        except Exception as e:
            log.exception('Something went wrong trying to persist the store to %s', self.store_path)
            raise e

    def load(self):
        loaded = self._from_json()
        loaded[FILE_HASH_TO_PATHNAMES] = defaultdict(list, loaded[FILE_HASH_TO_PATHNAMES])
        loaded[KNOWN_PATHNAMES_HASHES] = set(loaded[KNOWN_PATHNAMES_HASHES])
        self._data.update(loaded)

    def save(self):
        self._to_json()
