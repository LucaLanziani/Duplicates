# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys


class DummyOutput(object):

    def __init__(self):
        pass

    def status(self, *args):
        pass

    def print(self, *args, **kwdargs):
        pass


class ConsoleOutput(DummyOutput):
    """Report the status of process in the terminal"""
    def __init__(self):
        super(ConsoleOutput, self).__init__()

    def status(self, analized, filtered, total):
        percentage = 0
        if analized > 0:
            percentage = 100 / (filtered / analized)

        msg = '%%%(size)ss/%%%(size)ss/%%%(size)ss (%%5.2f%%%%) files' % {
            'size': len(str(total))
        }
        sys.stdout.write("\r")
        sys.stdout.write(msg % (
            analized,
            filtered,
            total,
            percentage
        ))
        sys.stdout.flush()

    def print(self, *args, **kwdargs):
        print(*args, **kwdargs)
