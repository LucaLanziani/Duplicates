#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from duplicates.fs.explorer import Explorer
from duplicates.libraries.utils import set_analyzed_directory_as_cwd
from duplicates.store.json_store import JsonStore


log = logging.getLogger(__name__)


class Indexer(Explorer):

    def __init__(self, directory, output=None, unix_patterns=None, storeCLS=None):
        if storeCLS is None:
            storeCLS = JsonStore
        super(Indexer, self).__init__(directory, output, unix_patterns, storeCLS)

    @set_analyzed_directory_as_cwd
    def index(self):
        for attrs in self._getattributes():
            self._store.add_file(attrs)
            self._progress(None, None)
        self._output.print()
        return self._store

    def purge(self):
        for hash, paths in self._store.paths_by_hash():
            for path in paths:
                if not os.path.isfile(path):
                    self._store.remove_pathname(path)
        self._store.save()

    def run(self, store=True):
        data = self.index()
        if store:
            data.save()
        return self
