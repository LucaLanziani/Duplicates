# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class DummyStore(object):

    """Store configurations on a json file"""
    def __init__(self, default_data):
        super(DummyStore, self).__init__()
        self._default_data = default_data
        self._data = None
        if self._default_data is None:
            self._default_data = {}

    def load(self):
        if self._data is None:
            self._data = self._default_data

    def save(self):
        pass
