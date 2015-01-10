from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys


class DummyOutput():

    def __init__(self):
        pass

    def status(self, analized, total):
        pass

    def print(self, *args, **kwdargs):
        pass


class ConsoleOutput(object):
    """Report the status of process in the terminal"""
    def __init__(self):
        super(ConsoleOutput, self).__init__()

    def status(self, analized, total):
        percentage = 0
        if analized > 0:
            percentage = 100/(total/analized)
        max_length = len(str(total))
        msg = '%%%ss/%%%ss (%%5.2f%%%%) files' % (max_length, max_length)
        sys.stdout.write("\r")
        sys.stdout.write(msg % (
            analized,
            total,
            percentage
        ))
        sys.stdout.flush()

    def print(self, *args, **kwdargs):
        print(*args, **kwdargs)
