#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os

from duplicates.fs.directory import Directory
from duplicates.fs.file_attr import Attributes, FileAttr
from duplicates.libraries.filters import UnixShellWildcardsFilter
from duplicates.libraries.output import DummyOutput
from duplicates.libraries.utils import DuplicateExceptions
from duplicates.store.json_store import InmemoryStore

ATTRIBUTES = set([Attributes.HASH, Attributes.SIZE, Attributes.LMTIME, Attributes.PATHNAME_HASH])

invalid_attributes = ATTRIBUTES.difference(FileAttr._attr_to_method().keys())
assert invalid_attributes == set([]), 'Those attributes do not exist %s' % invalid_attributes

log = logging.getLogger(__name__)


class FilterNotFoundException(DuplicateExceptions):
    pass


class FilterMismatchException(DuplicateExceptions):
    pass


class Explorer(object):

    def __init__(self, directory, output=None, unix_patterns=None, storeCLS=None):
        self._directory = os.path.abspath(os.path.expanduser(directory))
        self._settings(output, storeCLS)
        self._pathname_sha_cache = {}
        self._load_store_content()
        self._set_filters(unix_patterns)

    def _load_store_content(self):
        try:
            self._store.load()
        except Exception:
            log.debug("No existing store in directory %s", self._directory)

    def _set_filters(self, unix_patterns):
        if self._store.filters is None and not unix_patterns:
            raise FilterNotFoundException('You need to specify a filter the first time you index a directory')

        if unix_patterns and self._store.filters and (unix_patterns != self._store.filters):
            raise FilterMismatchException('Filters are already defined here %s' % self._store.filters)

        if not unix_patterns:
            unix_patterns = self._store.filters

        self._store.filters = unix_patterns
        self._unixpatterns_filter = UnixShellWildcardsFilter(*self._store.filters)

    def _settings(self, output, storeCLS):
        if storeCLS is None:
            storeCLS = InmemoryStore
        if output is None:
            output = DummyOutput()

        self._output = output
        self._store = storeCLS(self._directory)

    def _progress(self, signum, stack):
        analized = len(self._store)
        self._output.progress(analized, self._filtered, self._total_files)

    def _count_files(self):
        log.debug('Counting number of files in %s', self._directory)
        self._total_files = 0
        self._filtered = 0
        for directory, filepath in Directory.content(self._directory):
            self._total_files += 1
            if (self._valid_pathname(directory, filepath)):
                self._filtered += 1

    def _valid_pathname(self, directory, filepath):
        pathname = os.path.join(directory, filepath)
        return (
            pathname != self._store.store_path and
            os.path.isfile(pathname) and
            (not self._unixpatterns_filter.enabled or
                self._unixpatterns_filter.match(filepath))
        )

    def _getattributes(self):
        log.info('Indexing %s content with %s filters', self._directory, self._store.filters)
        self._count_files()
        filtered_content = self._filtered_content()
        log.info(
            'Indexing %d files (%s)',
            self._filtered - len(self._store),
            self._store.filters
        )
        return FileAttr.attr_generator(filtered_content, attributes=ATTRIBUTES)

    def _filtered_content(self):
        log.debug('Create generator for filtered pathnames')
        pathnames_generator = Directory.content(self._directory)
        filtered_pathnames_generator = self._unixpatterns_filter.filter_dircontent(pathnames_generator)
        return self._store.filter_known_files(filtered_pathnames_generator)

    def _pathnames(self):
        for pathname, _ in self._filtered_content():
            yield pathname

    def list(self):
        log.info('Listing %s content with %s filter', self._directory, self._store.filters)
        self._count_files()
        filtered_content = self._filtered_content()
        for content in filtered_content:
            yield content

    @property
    def directory(self):
        return self._directory
