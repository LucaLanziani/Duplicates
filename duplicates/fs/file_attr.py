# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import hashlib
import logging

import os
import stat

from duplicates.libraries.utils import absolute_path, DuplicateExceptions, relative_path

BLOCKSIZE = 65536

log = logging.getLogger(__name__)


class FileNotFoundError(DuplicateExceptions):
    pass


def file_exists(func):
    def func_wrapper(cls, pathname, *args, **kwargs):
        abs_pathname = absolute_path(pathname)
        if not os.path.exists(abs_pathname):
            raise FileNotFoundError(abs_pathname)
        return func(cls, pathname, *args, **kwargs)
    return func_wrapper


class FileAttr(object):
    """Return the file data"""

    @classmethod
    def _attr_to_method(cls):
        return {
            'sha256': cls._sha256,
            'sha1': cls._sha1,
            'md5': cls._md5,
            'hash': cls._hash,
            'abs_pathame': cls._abs_pathname,
            'directory': cls._directory,
            'filename': cls._filename,
            'extension': cls._extension,
            'abs_pathname_hash': cls._abs_pathname_hash,
            'size': cls._size,
            'lmtime': cls._lmtime,
            'pathname_hash': cls._pathname_hash
        }

    @classmethod
    @file_exists
    def _sha256(cls, pathname):
        return cls._hash(pathname, hash_function=hashlib.sha256)

    @classmethod
    @file_exists
    def _sha1(cls, pathname):
        return cls._hash(pathname, hash_function=hashlib.sha1)

    @classmethod
    @file_exists
    def _md5(cls, pathname):
        return cls._hash(pathname, hash_function=hashlib.md5)

    @classmethod
    @file_exists
    def _hash(cls, pathname, hash_function=hashlib.md5):
        log.debug('Hashing %s using %s algorithm', cls._abs_pathname, hash_function.__name__)
        filehash = hash_function()
        with open(absolute_path(pathname), 'rb') as fp:
            buf = fp.read(BLOCKSIZE)
            while len(buf) > 0:
                filehash.update(buf)
                buf = fp.read(BLOCKSIZE)
        return filehash.hexdigest()

    @classmethod
    @file_exists
    def _abs_pathname(cls, pathname):
        return absolute_path(pathname)

    @classmethod
    @file_exists
    def _pathname_hash(cls, pathname):
        return hashlib.sha256(pathname.encode('utf-8')).hexdigest()

    @classmethod
    @file_exists
    def _abs_pathname_hash(cls, pathname):
        return cls._pathname_hash(cls._abs_pathname(pathname))

    @classmethod
    @file_exists
    def _directory(cls, pathname):
        return os.path.dirname(cls._abs_pathname(pathname))

    @classmethod
    @file_exists
    def _filename(cls, pathname):
        return os.path.basename(cls._abs_pathname(pathname))

    @classmethod
    @file_exists
    def _extension(cls, pathname):
        return os.path.splitext(cls._abs_pathname(pathname))[1].lower()

    @classmethod
    @file_exists
    def _size(cls, pathname):
        return os.stat(cls._abs_pathname(pathname))[stat.ST_SIZE]

    @classmethod
    @file_exists
    def _lmtime(cls, pathname):
        return os.stat(cls._abs_pathname(pathname))[stat.ST_MTIME]

    @classmethod
    @file_exists
    def get(cls, pathname, directory, attributes=()):
        attrs_to_method = cls._attr_to_method()
        attrs = set(attrs_to_method.keys()).intersection(attributes)
        result = {
            'rootdir': absolute_path(directory),
            'pathname': relative_path(directory, pathname)
        }
        for attr in attrs:
            result[attr] = attrs_to_method[attr](cls._abs_pathname(pathname))
        return result

    @classmethod
    def attr_generator(cls, dircontent, attributes=None):
        if attributes is None:
            attributes = cls._attr_to_method().keys()
        for pathname, rootDir in dircontent:
            yield cls.get(pathname, rootDir, attributes=attributes)
