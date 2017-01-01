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

    def duplicates(self, index):
        for _, duplicates in index.paths_by_hash:
            if len(duplicates) > 1:
                yield duplicates

    def intersection(self, main_index, secondary_index):
        main_index_hashes = main_index.files_hashes
        secondary_index_hashes = secondary_index.files_hashes
        common_hashes = main_index_hashes.intersection(secondary_index_hashes)
        return [(main_index.abs_pathnames_from_hash(hash),
                 secondary_index.abs_pathnames_from_hash(hash)) for hash in common_hashes]

    def difference(self, main_index, secondary_index):
        main_index_hashes = main_index.files_hashes
        secondary_index_hashes = secondary_index.files_hashes
        difference = main_index_hashes.difference(secondary_index_hashes)
        list_of_list_of_paths = map(main_index.abs_pathnames_from_hash, difference)
        return [path for list_of_paths in list_of_list_of_paths for path in list_of_paths]
