#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usage: %(name)s [options] DIRECTORY [PATTERNS...]

You can filter the analyzed files passing multiple patterns through command
line, the patterns can include "Unix shell-style wildcards"

Options:
    --first_n N       stop after N files [default: inf]
    --verbose         print status update in console
    --no-store        do not save the gathered information on filesystem

Examples:
    %(name)s .                  # every file
    %(name)s . '*.png'          # only .png files
    %(name)s . '*.png' '*.jpg'  # .png and .jpg files
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from docopt import docopt
from duplicates.data_store import FileStore
from duplicates.directory import Directory
from duplicates.file_attr import FileAttrFactory
from duplicates.filters import UnixShellWildcardsFilter
from duplicates.output import ConsoleOutput, DummyOutput
from schema import And, Optional, Or, Schema, SchemaError, Use


class Duplicates():

    def __init__(self, opt):
        self._parse_opt(opt)
        self._store = FileStore(self._directory.pathname)
        self._pathname_sha_cache = {}

    def _parse_opt(self, opt):
        self.output = DummyOutput()
        if opt["--verbose"]:
            self.output = ConsoleOutput()
        self._unixpatterns_filter = UnixShellWildcardsFilter(opt['PATTERNS'])
        self._first_n = float(opt['--first_n'])
        self._directory = Directory(opt['DIRECTORY'])
        self._allow_save = not opt['--no-store']

    def _print_state(self, signum, stack):
        analized = len(self._store.known_pathnames)
        self.output.status(analized, self._filtered, self._total_files)

    def _file_number(self):
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
            pathname_filter=self._valid_pathname,
            limit=self._first_n
        )
        for pathname in content:
            yield pathname

    def collect_data(self):
        for pathname in self._file_list():
            self._store.add_file(FileAttrFactory.by_pathname(pathname))
            self._print_state(None, None)
        self.output.print()

    def _initialize(self):
        self._file_number()

    def _terminate(self):
        if self._allow_save:
            self._store.save()

    def run(self):
        self._initialize()
        self.collect_data()
        self._terminate()


def validate_args(opt):
    schema = Schema({
        'DIRECTORY': And(os.path.exists, error="DIRECTORY does not exists"),
        '--first_n': Or(u'inf', And(Use(int)),
                        error="--first_n=N should be integer"),
        Optional('--verbose'): bool,
        Optional('--no-store'): bool,
        Optional('PATTERNS'): [str]
    })
    try:
        opt = schema.validate(opt)
    except SchemaError as e:
        exit(e)
    return opt


def run(name=None):
    if name is None:
        name = __file__
    opt = docopt(__doc__ % {'name': name}, argv=None, help=True,
                 version=None, options_first=False)
    opt = validate_args(opt)
    Duplicates(opt).run()


if __name__ == '__main__':
    run()
