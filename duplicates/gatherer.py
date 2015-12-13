#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from duplicates.fs.directory import Directory
from duplicates.fs.file_attr import FileAttr
from duplicates.libraries.filters import UnixShellWildcardsFilter
from duplicates.libraries.output import DummyOutput
from duplicates.store.inmemory_store import InmemoryStore

log = logging.getLogger(__name__)

ATTRIBUTES = set(['hash', 'abs_pathame', 'directory', 'filename', 'extension', 'abs_pathname_hash', 'size',
                  'lmtime', 'pathname_hash'])

invalid_attributes = ATTRIBUTES.difference(FileAttr._attr_to_method().keys())
assert invalid_attributes == set([]), 'Those attributes do not exist %s' % invalid_attributes


class Gatherer(object):

    def __init__(self, directory, output=None, unix_patterns=None, store=None):
        self._settings(output, unix_patterns, store)
        self._directory = directory
        self._pathname_sha_cache = {}

    def _settings(self, output, unix_patterns, store):
        if store is None:
            store = InmemoryStore
        if output is None:
            output = DummyOutput()
        if not unix_patterns:
            unix_patterns = ['*']

        self._output = output
        self._store = store()
        self._unixpatterns_filter = UnixShellWildcardsFilter(*unix_patterns)

    def _progress(self, signum, stack):
        analized = len(self._store)
        self._output.progress(analized, self._filtered, self._total_files)

    def _count_files(self):
        self._total_files = 0
        self._filtered = 0
        for directory, filepath in Directory.content(self._directory):
            self._total_files += 1
            if (self._valid_pathname(filepath)):
                self._filtered += 1

    def _valid_pathname(self, pathname):
        return (
            pathname != self._store.store_path and
            os.path.isfile(pathname) and
            (not self._unixpatterns_filter.enabled or
                self._unixpatterns_filter.match(pathname))
        )

    def _filtered_content(self):
        content = Directory.content(self._directory)
        return self._unixpatterns_filter.filter_dircontent(content)

    def _pathnames(self):
        for _, pathname in self._filtered_content():
            yield pathname

    def collect_data(self):
        """
        Collect files data and return the store object
        """
        self._count_files()
        filtered_content = self._filtered_content()
        for attrs in FileAttr.attr_generator(filtered_content, attributes=ATTRIBUTES):
            self._store.add_file(attrs)
            self._progress(None, None)
        self._output.print()
        return self._store

    def print_duplicates(self):
        for _, duplicates in self._store.paths_by_hash():
            if len(duplicates) > 1:
                self._output.print('\t'.join(duplicates))

    def print_content(self):
        for filepath in self._pathnames():
            self._output.print(filepath)

    def run(self, store=True):
        data = self.collect_data()
        if store:
            data.save()
        return self
