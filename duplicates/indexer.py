#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from duplicates.fs.explorer import Explorer
from duplicates.store.json_store import JsonStore


log = logging.getLogger(__name__)


class Indexer(Explorer):

    def __init__(self, directory, output=None, unix_patterns=None, storeCLS=None):
        if storeCLS is None:
            storeCLS = JsonStore
        super(Indexer, self).__init__(directory, output, unix_patterns, storeCLS)

    def __len__(self):
        return len(self._store)

    def index(self):
        for attrs in self._getattributes():
            self._store.add_file(attrs)
            self._progress(None, None)
        self._output.print()
        return self

    def purge(self):
        for hash, paths in self._store.relpaths_by_hash():
            for path in paths:
                if not os.path.isfile(os.path.join(self.directory, path)):
                    self._store.remove_pathname(path)
        self._store.clean()
        return self

    def run(self, persist=True):
        self.index()
        if persist:
            self.save()
        return self

    def save(self):
        self._store.save()

    @property
    def files_hashes(self):
        return set(self._store.hash_to_pathnames.keys())

    def abs_pathnames_from_hash(self, hash):
        return self._store.hash_to_abs_pathnames(hash)

    @property
    def last_update(self):
        return self._store.last_update

    @property
    def paths_by_hash(self):
        return self._store.paths_by_hash()
