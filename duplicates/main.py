#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from docopt import docopt
from duplicates.data_store import FileStore
from duplicates.directory import Directory
from duplicates.file_attr import FileAttrFactory
from duplicates.filters import UnixShellWildcardsFilter
from duplicates.output import ConsoleOutput, DummyOutput
from schema import And, Optional, Schema, SchemaError


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
        self._unixpatterns_filter = UnixShellWildcardsFilter(unix_patterns)

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


class CommandLineInterface(object):
    """Usage: %(name)s [options] DIRECTORY [PATTERNS...]

    You can filter the analyzed files passing multiple patterns through command
    line, the patterns can include "Unix shell-style wildcards"

    Options:
        --verbose         print status update in console
        --no-store        do not save the gathered information on filesystem

    Examples:
        %(name)s .                  # every file
        %(name)s . '*.png'          # only .png files
        %(name)s . '*.png' '*.jpg'  # .png and .jpg files
    """

    def __init__(self):
        super(CommandLineInterface, self).__init__()

    def _validate_args(self, opt):
        schema = Schema({
            'DIRECTORY': And(os.path.exists, error="Dir does not exists"),
            Optional('--verbose'): bool,
            Optional('--no-store'): bool,
            Optional('PATTERNS'): [str]
        })
        try:
            opt = schema.validate(opt)
        except SchemaError as e:
            exit(e)
        return opt

    def _parse_args(self, name=None):
        if name is None:
            name = __file__
        opt = docopt(self.__doc__ % {'name': name}, argv=None, help=True,
                     version=None, options_first=False)
        return self._validate_args(opt)

    def run(self, name=None):
        opt = self._parse_args(name)
        Duplicates(
            opt['DIRECTORY'],
            verbose=opt['--verbose'],
            unix_patterns=opt['PATTERNS']
        ).run(not opt['--no-store'])

if __name__ == '__main__':
    CommandLineInterface().run()
