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


def absolute_path(directory):
    directory = os.path.expanduser(directory)
    directory = os.path.expandvars(directory)
    directory = os.path.normpath(directory)
    return os.path.abspath(directory)


def serialize_date(date):
    return date.strftime(DATE_FORMAT)


def deserialize_date(str_date):
    return datetime.strptime(str_date, DATE_FORMAT)


epoch = datetime(*EPOCH)
