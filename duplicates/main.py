#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from duplicates.data_store import FileStore
from duplicates.directory import Directory
from duplicates.file_attr import FileAttrFactory
from duplicates.filters import UnixShellWildcardsFilter
from duplicates.output import ConsoleOutput, DummyOutput


class Duplicates():

    def __init__(self, directory, verbose=False, unix_patterns=None):
        self._settings(verbose, unix_patterns)
        self._directory = Directory(directory)
        self._store = FileStore(self._directory.pathname)
        self._pathname_sha_cache = {}

    def _settings(self, verbose, unix_patterns):
        self.output = DummyOutput()
        if verbose:
            self.output = ConsoleOutput()
        if not unix_patterns:
            unix_patterns = ['*']
        self._unixpatterns_filter = UnixShellWildcardsFilter(*unix_patterns)

    def _print_state(self, signum, stack):
        analized = len(self._store)
        self.output.status(analized, self._filtered, self._total_files)

    def _get_file_number(self):
        self._content = list(self._directory.dir_content())
        self._total_files = len(self._content)
        self._filtered = len(filter(self._valid_pathname, self._content))

    def _valid_pathname(self, pathname):
        return (
            pathname != self._store.store_path and
            os.path.isfile(pathname) and
            (not self._unixpatterns_filter.enabled or
                self._unixpatterns_filter.match(pathname))
        )

    def _file_list(self):
        content = self._directory.dir_content(
            pathname_filter=self._valid_pathname
        )
        for pathname in content:
            yield pathname

    def collect_data(self):
        """
        Collect files data and return the store object
        """
        self._get_file_number()
        for pathname in self._file_list():
            self._store.add_file(FileAttrFactory.by_pathname(pathname))
            self._print_state(None, None)
        self.output.print()
        return self._store

    def run(self, store=True):
        data = self.collect_data()
        if store:
            data.save()
        return data
