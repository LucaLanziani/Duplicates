#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from duplicates.libraries.output import DummyOutput
from duplicates.store.json_store import JsonStore, StoreNotFoundError

log = logging.getLogger(__name__)


class Analyzer(object):

    def __init__(self, directory, output=None):
        self._directory = directory
        self._pathname_sha_cache = {}
        self._store = self._load_store(directory)
        self.output = output
        if output is None:
            self.output = DummyOutput()

    def duplicates(self):
        for _, duplicates in self._store.paths_by_hash():
            if len(duplicates) > 1:
                yield duplicates

    def _load_store(self, directory):
        store = JsonStore(directory)
        if (not store.exists):
            msg = "Can't find any index, please run the software with --index for the following directory:"
            log.error(msg + " %s", directory)
            excp = StoreNotFoundError(msg, directory)
            excp.message = msg + " %s" % (directory)
            excp.exit_code = os.EX_NOINPUT
            raise excp
        return store

    def intersection(self, directory):
        store = self._load_store(directory)
        common = set(self._store.hash_to_pathnames.keys()).intersection(set(store.hash_to_pathnames.keys()))
        for hash in common:
            self.output.print("%s -> %s" % (self._store.hash_to_abs_pathnames(hash),
                                            store.hash_to_abs_pathnames(hash)))

    def difference(self, directory):
        store = self._load_store(directory)
        difference = set(self._store.hash_to_pathnames.keys()).difference(set(store.hash_to_pathnames.keys()))
        for hash in difference:
            self.output.print("%s" % '\n'.join(self._store.hash_to_abs_pathnames(hash)))
