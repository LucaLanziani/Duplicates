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

    def __init__(self, output=None):
        self.output = output
        if output is None:
            self.output = DummyOutput()

    def duplicates(self, store):
        for _, duplicates in store.paths_by_hash():
            if len(duplicates) > 1:
                yield duplicates

    def intersection(self, store, second_store):
        common = set(store.hash_to_pathnames.keys()).intersection(set(second_store.hash_to_pathnames.keys()))
        results = []
        for hash in common:
            results.append((store.hash_to_abs_pathnames(hash), second_store.hash_to_abs_pathnames(hash)))
        return results

    def difference(self, store, second_store):
        difference = set(store.hash_to_pathnames.keys()).difference(set(second_store.hash_to_pathnames.keys()))
        results = []
        for hash in difference:
            results.append(store.hash_to_abs_pathnames(hash))
        return results