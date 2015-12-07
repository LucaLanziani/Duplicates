# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import hashlib
import logging

import os
import stat

from duplicates.libraries.utils import absolute_path, DuplicateExceptions

BLOCKSIZE = 65536

log = logging.getLogger(__name__)


class FileNotFoundError(DuplicateExceptions):
    pass


def cache_result(func):
    """
    Decorator to cache the return value of a give function

    :param func:
    :return: return the cached value returned by the given function
    """

    def _decorator(self, *args, **kwargs):
        key = func.__name__
        try:
            value = self._cached[key]
            log.debug('Return the cached value of %s', key)
            return value
        except KeyError:
            self._cached[key] = func(self, *args, **kwargs)
            return self._cached[key]
    return _decorator


class FileAttr(object):
    """Return the file data"""
    def __init__(self, pathname):
        super(FileAttr, self).__init__()
        self._abs_pathname = absolute_path(pathname)
        if not os.path.exists(self._abs_pathname):
            raise FileNotFoundError(pathname)
        self._cached = {}

    def _hash(self, hash_function=hashlib.md5):
        log.debug('Hashing %s using %s algorithm', self._abs_pathname, hash_function.__name__)
        filehash = hash_function()
        with open(self._abs_pathname, 'rb') as fp:
            buf = fp.read(BLOCKSIZE)
            while len(buf) > 0:
                filehash.update(buf)
                buf = fp.read(BLOCKSIZE)
        return filehash.hexdigest()

    @property
    def pathname(self):
        return self._abs_pathname

    @property
    def directory(self):
        return os.path.dirname(self._abs_pathname)

    @property
    def filename(self):
        return os.path.basename(self._abs_pathname)

    @property
    def extention(self):
        return os.path.splitext(self._abs_pathname)[1].lower()

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
    @cache_result
    def abs_pathname_hash(self):
        return FileAttr.hash_pathname(self._abs_pathname)

    @property
    def size(self):
        return os.stat(self._abs_pathname)[stat.ST_SIZE]

    @property
    def lmtime(self):
        return os.stat(self._abs_pathname)[stat.ST_MTIME]

    @staticmethod
    def hash_pathname(pathname):
        return hashlib.sha256(pathname.encode('utf-8')).hexdigest()

    def similar(self, other):
        return (
            self.extention == other.extention and
            self.size == other.size and
            self.lmtime == other.lmtime
        )


class FileAttrFactory(object):
    """Generate FileAttr object"""

    filesAttr = {}

    @classmethod
    def by_pathname(cls, pathname):
        abs_pathname = absolute_path(pathname)
        store = cls.filesAttr
        file_attr = FileAttr(abs_pathname)
        key = file_attr.abs_pathname_hash
        if (key not in store or not store[key].similar(file_attr)):
            cls.filesAttr[key] = file_attr

        return cls.filesAttr[key]
