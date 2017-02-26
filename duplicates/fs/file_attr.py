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


class Attributes:
    SHA256 = 'sha256'
    SHA1 = 'sha1'
    MD5 = 'md5'
    HASH = 'hash'
    ABS_PATHAME = 'abs_pathame'
    DIRECTORY = 'directory'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    ABS_PATHNAME_HASH = 'abs_pathname_hash'
    SIZE = 'size'
    LMTIME = 'lmtime'
    PATHNAME_HASH = 'pathname_hash'
    PATHNAME = 'pathname'
    ROOTDIR = 'rootdir'


class FileNotFoundError(DuplicateExceptions):
    pass


def file_exists(func):
    def func_wrapper(cls, directory, pathname, *args, **kwargs):
        abs_pathname = absolute_path(directory, pathname)
        if not os.path.exists(abs_pathname):
            raise FileNotFoundError('Cannot find %s' % abs_pathname)
        return func(cls, directory, pathname, *args, **kwargs)
    return func_wrapper


class FileAttr(object):
    """Return the file data"""

    @classmethod
    def _attr_to_method(cls):
        return {
            Attributes.SHA256: cls._sha256,
            Attributes.SHA1: cls._sha1,
            Attributes.MD5: cls._md5,
            Attributes.HASH: cls._hash,
            Attributes.ABS_PATHAME: cls._abs_pathname,
            Attributes.DIRECTORY: cls._directory,
            Attributes.FILENAME: cls._filename,
            Attributes.EXTENSION: cls._extension,
            Attributes.ABS_PATHNAME_HASH: cls._abs_pathname_hash,
            Attributes.SIZE: cls._size,
            Attributes.LMTIME: cls._lmtime,
            Attributes.PATHNAME_HASH: cls._pathname_hash
        }

    @classmethod
    @file_exists
    def _sha256(cls, directory, pathname):
        return cls._hash(directory, pathname, hash_function=hashlib.sha256)

    @classmethod
    @file_exists
    def _sha1(cls, directory, pathname):
        return cls._hash(directory, pathname, hash_function=hashlib.sha1)

    @classmethod
    @file_exists
    def _md5(cls, directory, pathname):
        return cls._hash(directory, pathname, hash_function=hashlib.md5)

    @classmethod
    @file_exists
    def _hash(cls, directory, pathname, hash_function=hashlib.md5):
        log.debug('Hashing %s using %s algorithm', pathname, hash_function.__name__)
        filehash = hash_function()
        with open(absolute_path(directory, pathname), 'rb') as fp:
            buf = fp.read(BLOCKSIZE)
            while len(buf) > 0:
                filehash.update(buf)
                buf = fp.read(BLOCKSIZE)
        log.debug('result: %s', filehash.hexdigest())
        return filehash.hexdigest()

    @classmethod
    def _hash_string(cls, string, hash_function=hashlib.sha256):
        return hash_function(string.encode('utf-8')).hexdigest()

    @classmethod
    @file_exists
    def _abs_pathname(cls, directory, pathname):
        return absolute_path(directory, pathname)

    @classmethod
    def _pathname_hash(cls, directory, pathname):
        assert not os.path.isabs(pathname)
        return cls._hash_string(pathname)

    @classmethod
    def _abs_pathname_hash(cls, directory, pathname):
        return cls._hash_string(cls._abs_pathname(directory, pathname))

    @classmethod
    @file_exists
    def _directory(cls, directory, pathname):
        return os.path.dirname(cls._abs_pathname(directory, pathname))

    @classmethod
    @file_exists
    def _filename(cls, directory, pathname):
        return os.path.basename(cls._abs_pathname(directory, pathname))

    @classmethod
    @file_exists
    def _extension(cls, directory, pathname):
        return os.path.splitext(cls._abs_pathname(directory, pathname))[1].lower()

    @classmethod
    @file_exists
    def _size(cls, directory, pathname):
        return os.stat(cls._abs_pathname(directory, pathname))[stat.ST_SIZE]

    @classmethod
    @file_exists
    def _lmtime(cls, directory, pathname):
        return os.stat(cls._abs_pathname(directory, pathname))[stat.ST_MTIME]

    @classmethod
    def pathname_hash(cls, *args, **kwdargs):
        return cls._pathname_hash(*args, **kwdargs)

    @classmethod
    @file_exists
    def get(cls, directory, filepath, attributes=()):
        assert os.path.isdir(directory)
        attrs_to_method = cls._attr_to_method()
        attrs = set(attrs_to_method.keys()).intersection(attributes)
        rel_pathname = relative_path(directory, filepath)
        result = {
            Attributes.ROOTDIR: absolute_path(directory),
            Attributes.PATHNAME: rel_pathname
        }
        for attr in attrs:
            result[attr] = attrs_to_method[attr](absolute_path(directory), rel_pathname)
        return result

    @classmethod
    def attr_generator(cls, dircontent, attributes=None):
        if attributes is None:
            attributes = cls._attr_to_method().keys()
        for rootDir, filepath in dircontent:
            yield cls.get(rootDir, filepath, attributes=attributes)
