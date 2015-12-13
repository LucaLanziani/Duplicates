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


def absolute_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.normpath(path)
    return os.path.abspath(path)


def relative_path(directory, path):
    abs_directory = absolute_path(directory)
    abs_path = absolute_path(path)
    return os.path.relpath(abs_path, abs_directory)


def serialize_date(date):
    return date.strftime(DATE_FORMAT)


def deserialize_date(str_date):
    return datetime.strptime(str_date, DATE_FORMAT)


epoch = datetime(*EPOCH)
