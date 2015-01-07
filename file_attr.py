from __future__ import (absolute_import, print_function, unicode_literals,
                        division)

import os
import hashlib
import stat

from utils import absolute_path

BLOCKSIZE = 65536


class FileNotFoundError(Exception):
    pass


def cache_result(func):
    def _decorator(self, *args, **kwargs):
        key = func.__name__
        try:
            return self._cached[key]
        except KeyError:
            self._cached[key] = func(self, *args, **kwargs)
            return self._cached[key]
    return _decorator


class FileAttr(object):
    """Return the file data"""
    def __init__(self, pathname):
        super(FileAttr, self).__init__()
        self.abs_pathname = absolute_path(pathname)
        if not os.path.exists(self.abs_pathname):
            raise FileNotFoundError(pathname)
        self._cached = {}

    def extention(self):
        return os.path.splitext(self.abs_pathname)[1].lower()

    def _hash(self, hash_function=hashlib.md5):
        filehash = hash_function()
        with open(self.abs_pathname, 'rb') as fp:
            buf = fp.read(BLOCKSIZE)
            while len(buf) > 0:
                filehash.update(buf)
                buf = fp.read(BLOCKSIZE)
        return filehash.hexdigest()

    @property
    def hash(self):
        return self.md5

    @property
    @cache_result
    def sha256(self):
        return self._hash(hash_function=hashlib.sha256)

    @property
    @cache_result
    def sha1(self):
        return self._hash(hash_function=hashlib.sha1)

    @property
    @cache_result
    def md5(self):
        return self._hash(hash_function=hashlib.md5)

    @property
    def size(self):
        return os.stat(self.abs_pathname)[stat.ST_SIZE]

    @property
    def lmtime(self):
        return os.stat(self.abs_pathname)[stat.ST_MTIME]

    def similar(self, other):
        return (self.size == other.size and self.lmtime == other.lmtime)

    @staticmethod
    def hash_pathname(pathname):
        return hashlib.sha256(pathname).hexdigest()


class FileAttrFactory(object):
    """Generate FileAttr object"""

    filesAttr = {}

    def __init__(self):
        super(FileAttrFactory, self).__init__()

    @classmethod
    def by_pathname(cls, pathname):
        pathname = absolute_path(pathname)
        store = cls.filesAttr
        file_attr = FileAttr(pathname)
        key = FileAttr.hash_pathname(pathname)
        if (key not in store or not store[key].similar(file_attr)):
            cls.filesAttr[key] = file_attr

        return cls.filesAttr[key]
