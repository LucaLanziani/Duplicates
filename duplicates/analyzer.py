#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from duplicates.libraries.output import DummyOutput

log = logging.getLogger(__name__)


class Analyzer(object):

    def __init__(self, output=None):
        self.output = output
        if output is None:
            self.output = DummyOutput()

    def duplicates(self, store):
        for _, duplicates in store.paths_by_hash():
            if len(duplicates) > 1:
                yield duplicates

    def _get_files_hashes(self, store):
        return set(store.hash_to_pathnames.keys())

    def intersection(self, main_store, secondary_store):
        main_store_hashs = self._get_files_hashes(main_store)
        secondary_store_hashs = self._get_files_hashes(secondary_store)
        common_hashs = main_store_hashs.intersection(secondary_store_hashs)
        return [(main_store.hash_to_abs_pathnames(hash),
                 secondary_store.hash_to_abs_pathnames(hash)) for hash in common_hashs]

    def difference(self, main_store, secondary_store):
        main_store_hashes = self._get_files_hashes(main_store)
        secondary_store_hashs = self._get_files_hashes(secondary_store)
        file_hashes = main_store_hashes.difference(secondary_store_hashs)
        list_of_list_of_paths = map(main_store.hash_to_abs_pathnames, file_hashes)
        return [path for list_of_paths in list_of_list_of_paths for path in list_of_paths]

    def get_indexed(self, store):
        for abs_pathname in store.list_of_abs_pathnames():
            yield abs_pathname
