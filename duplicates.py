#!/usr/bin/env python2
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from data_store import FileStore, FILESTORE
from file_attr import FileAttrFactory
from utils import absolute_path

WHITELISTED_EXTENTIONS = ['.gif', '.jpeg', '.jpg', '.png']


class Duplicates():

    def __init__(self, args, store):
        self._show_progress = self._pass
        self._first_n = float(args['first_n'])
        self.directory = absolute_path(args['DIRECTORY'])
        self.store = store
        self._pathname_sha_cache = {}

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

    def list(self):
        for pathname in self.dir_content():
            file_obj = FileAttrFactory.by_pathname(pathname)
            print(file_obj.pathname)

    def collect_data(self):
        for pathname in self.dir_content():
            self.store.add_file(FileAttrFactory.by_pathname(pathname))
            self._show_progress()


def main(args):
    try:
        store = FileStore(args)
        duplicates = Duplicates(args, store)
        duplicates.collect_data()
    except KeyboardInterrupt:
        store.save()
    else:
        store.save()

if __name__ == '__main__':
    main({'DIRECTORY': '.', 'first_n': 'inf'})
