#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Usage: duplicates.py [options] DIRECTORY

Options:
    --first_n N         stop after N files [default: inf]
    --clean             remove deleted file from the index  # TODO
    --progress          show the progress  # TODO
    --dry-run           display the pathnames  # TODO
    --find-file         find duplicates of a given file  # TODO
    --list              list all files in the given directory  # TODO
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from data_store import FileStore, FILESTORE
from docopt import docopt
from file_attr import FileAttrFactory
from utils import absolute_path
from schema import And, Optional, Or, Schema, SchemaError, Use


WHITELISTED_EXTENTIONS = ['.gif', '.jpeg', '.jpg', '.png']


class Duplicates():

    def __init__(self, opt):
        self._parse_opt(opt)
        self._show_progress = self._pass
        self._store = FileStore(self.directory)
        self._pathname_sha_cache = {}

    def _parse_opt(self, opt):
        self._first_n = float(opt['--first_n'])
        self.directory = absolute_path(opt['DIRECTORY'])

    def _pass(self):
        pass

    def dir_content(self, recursive=True):
        """
        yield white-listed files in the passed directory

        Args:
            recursive: navigate recursively all the directory tree
            first_n: limit the number of files return by this function
        """

        first_n = self._first_n
        whitelist_ext = set(WHITELISTED_EXTENTIONS)
        for pathname in self._dir_content(recursive):
            if first_n > 0:
                if os.path.splitext(pathname)[1].lower() in whitelist_ext:
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
            self._show_progress()

    def run(self):
        try:
            self.collect_data()
        except KeyboardInterrupt:
            self._store.save()
        else:
            self._store.save()


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
        Optional('--list'): bool
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
