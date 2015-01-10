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
import signal

from data_store import FileStore, FILESTORE
from docopt import docopt
from file_attr import FileAttrFactory
from output import ConsoleOutput, DummyOutput
from schema import And, Optional, Or, Schema, SchemaError, Use
from utils import absolute_path


class Duplicates():

    def __init__(self, opt):
        self._parse_opt(opt)
        self._store = FileStore(self.directory)
        self._pathname_sha_cache = {}

    def _parse_opt(self, opt):
        self.output = DummyOutput()
        if opt["--verbose"]:
            self.output = ConsoleOutput()
        self._extensions = set(opt['<ext>'])
        self._first_n = float(opt['--first_n'])
        self.directory = absolute_path(opt['DIRECTORY'])

    def _print_state(self, signum, stack):
        analized = len(self._store.known_pathnames)
        self.output.status(analized, self._total_files)

    def _file_number(self):
        first_n = self._first_n
        self._total_files = len(list(self.dir_content()))
        self._first_n = first_n

    def dir_content(self, recursive=True):
        """
        yield white-listed files in the passed directory

        Args:
            recursive: navigate recursively all the directory tree
            first_n: limit the number of files return by this function
        """

        first_n = self._first_n
        for pathname in self._dir_content(recursive):
            if first_n > 0:
                if (not self._extensions or
                   os.path.splitext(pathname)[1].lower() in self._extensions):
                    yield pathname
                    first_n -= 1
            else:
                break

    def _dir_content(self, recursive=True):
        dir_name = self.directory
        for root, dirs, files in os.walk(unicode(dir_name)):
            excluded_dirs = []
            for directory in dirs:
                if os.path.exists(os.path.join(root, directory, FILESTORE)):
                    excluded_dirs.append(directory)

            for folder in excluded_dirs:
                dirs.remove(folder)

            for name in files:
                yield os.path.join(root, name)
            if not recursive:
                break

    def collect_data(self):
        for pathname in self.dir_content():
            self._store.add_file(FileAttrFactory.by_pathname(pathname))
            self._print_state(None, None)
        self.output.print()

    def run(self):
        self._file_number()
        signal.signal(signal.SIGUSR1, self._print_state)
        try:
            self.collect_data()
        except KeyboardInterrupt:
            self._store.save()
        else:
            self._store.save()
            self.output.print("Saving the result")


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
        Optional('<ext>'): []
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
