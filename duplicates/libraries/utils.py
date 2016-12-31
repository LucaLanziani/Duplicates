# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from datetime import datetime

EPOCH = (1970, 1, 1)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
APPNAME = 'duplicates'


class DuplicateExceptions(Exception):
    pass


def set_analyzed_directory_as_cwd(func):
    def _decorator(self, *args, **kwargs):
        cwd = os.getcwd()
        os.chdir(self._directory)
        try:
            return func(self, *args, **kwargs)
        finally:
            os.chdir(cwd)
    return _decorator


def absolute_path(directory, filepath=None):
    path = directory
    if filepath is not None:
        path = os.path.join(directory, filepath)
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.normpath(path)
    return os.path.abspath(path)


def relative_path(directory, path):
    abs_directory = absolute_path(directory)
    abs_path = absolute_path(abs_directory, path)
    return os.path.relpath(abs_path, abs_directory)


def serialize_date(date):
    return date.strftime(DATE_FORMAT)


def deserialize_date(str_date):
    return datetime.strptime(str_date, DATE_FORMAT)


epoch = datetime(*EPOCH)
