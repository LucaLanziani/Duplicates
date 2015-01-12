#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Usage: duplicates.py [options] DIRECTORY [<ext>...]

You can filter the analyzed files passing multiple extensions to the software

Options:
    --first_n N         stop after N files [default: inf]
    --verbose           print status update in console
    --clean             remove deleted file from the index  # TODO
    --progress          show the progress  # TODO
    --dry-run           display the pathnames  # TODO
    --find-file         find duplicates of a given file  # TODO
    --list              list all files in the given directory  # TODO

Examples:
    ./duplicates.py .            # every file
    ./duplicates.py . .png       # only .png files
    ./duplicates.py . .png .jpg  # .png and .jpg files
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from docopt import docopt
from data_store import FileStore
from directory import Directory
from file_attr import FileAttrFactory
from output import ConsoleOutput, DummyOutput
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
        self._extensions = set(opt['<ext>'])
        self._first_n = float(opt['--first_n'])
        self._directory = Directory(opt['DIRECTORY'])

    def _print_state(self, signum, stack):
        analized = len(self._store.known_pathnames)
        self.output.status(analized, self._total_files)

    def _file_number(self):
        self._content = list(self._directory.dir_content())
        self._total_files = len(self._content)
        self._filtered = len(filter(self._valid_pathname, self._content))

    def _valid_pathname(self, pathname):
        return (
            pathname != self._store.store_path and
            os.path.isfile(pathname) and
            (not self._extensions or
                os.path.splitext(pathname)[1].lower() in self._extensions)
        )

    def collect_data(self):
        content = self._directory.dir_content(
            pathname_filter=self._valid_pathname,
            limit=self._first_n
        )
        for pathname in content:
            self._store.add_file(FileAttrFactory.by_pathname(pathname))
            self._print_state(None, None)
        self.output.print()

    def _initialize(self):
        self._file_number()

    def _terminate(self):
        self._store.save()

    def run(self):
        self._initialize()
        self.collect_data()
        self._terminate()


def main(opt):
    opt = validate_args(opt)
    Duplicates(opt).run()


def validate_args(opt):
    schema = Schema({
        'DIRECTORY': And(os.path.exists, error="DIRECTORY does not exists"),
        '--first_n': Or(u'inf', And(Use(int)),
                        error="--first_n=N should be integer"),
        Optional('--clean'): bool,
        Optional('--progress'): bool,
        Optional('--dry-run'): bool,
        Optional('--find-file'): bool,
        Optional('--list'): bool,
        Optional('--verbose'): bool,
        Optional('<ext>'): [
            And(
                str,
                Use(str.lower),
                lambda s: s.startswith('.'),
                error="Did you remember the dot?")
        ]
    })
    try:
        opt = schema.validate(opt)
    except SchemaError as e:
        exit(e)
    return opt

if __name__ == '__main__':
    opt = docopt(__doc__, argv=None, help=True,
                 version=None, options_first=False)
    main(opt)
