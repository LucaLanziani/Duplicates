# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys


def noop(*args, **kwdargs):
    pass


class DummyOutput(object):

    def __init__(self, *args, **kwdargs):
        pass

    def progress(self, *args):
        pass

    def print(self, *args, **kwdargs):
        pass


class ConsoleOutput(DummyOutput):
    """Report the status of process in the terminal"""
    def __init__(self, output, progress, **kwdargs):
        super(ConsoleOutput, self).__init__(output, progress, **kwdargs)

        if not output:
            self.print = noop

        if not progress:
            self.progress = noop

    def progress(self, analized, filtered, total):
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
