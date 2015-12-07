from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest
from datetime import datetime

from duplicates.libraries.utils import absolute_path, deserialize_date, serialize_date
from nose.tools import eq_

DATE_TIME = '1970-01-01T00:00:00.000000Z'


class UtilsTests(unittest.TestCase):

    def test_absolute_path(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.normpath(os.path.join(current_dir, '..'))
        eq_(absolute_path('.'), parent_dir)

    def test_deserialize_date(self):
        eq_(deserialize_date(DATE_TIME), datetime(1970, 1, 1))

    def test_serialize_date(self):
        eq_(serialize_date(datetime(1970, 1, 1)), DATE_TIME)
