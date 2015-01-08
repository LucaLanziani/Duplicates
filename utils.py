from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from datetime import datetime

EPOCH = (1970, 1, 1)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def absolute_path(directory):
    directory = os.path.expanduser(directory)
    directory = os.path.expandvars(directory)
    directory = os.path.normpath(directory)
    return os.path.abspath(directory)


def print_file_content():
    with open('./test/.duplicates.json.gz') as fd:
        content = fd.read(1)
        while len(content) > 0:
            print("%x %s", content, type(content))
            content = fd.read(1)


def serialize_date(date):
    return date.strftime(DATE_FORMAT)


def deserialize_date(str_date):
    return datetime.strptime(str_date, DATE_FORMAT)


epoch = datetime(*EPOCH)


if __name__ == '__main__':
    print_file_content()
