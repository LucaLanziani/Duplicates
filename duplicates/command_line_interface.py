#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from docopt import docopt
from duplicates.main import Duplicates
from schema import And, Optional, Schema, SchemaError


class CommandLineInterface(object):
    """Usage: %(name)s [options] DIRECTORY [PATTERNS...]

    You can filter the analyzed files passing multiple patterns through command
    line, the patterns can include "Unix shell-style wildcards"

    Options:
        --verbose         print status update in console
        --no-store        do not save the gathered information on filesystem

    Examples:
        %(name)s .                  # every file
        %(name)s . '*.png'          # only .png files
        %(name)s . '*.png' '*.jpg'  # .png and .jpg files
    """

    def __init__(self):
        super(CommandLineInterface, self).__init__()

    def _validate_args(self, opt):
        schema = Schema({
            'DIRECTORY': And(os.path.exists, error="Dir does not exists"),
            Optional('--verbose'): bool,
            Optional('--no-store'): bool,
            Optional('PATTERNS'): [str]
        })
        try:
            opt = schema.validate(opt)
        except SchemaError as e:
            exit(e)
        return opt

    def _parse_args(self, name=None):
        if name is None:
            name = __file__
        opt = docopt(self.__doc__ % {'name': name}, argv=None, help=True,
                     version=None, options_first=False)
        return self._validate_args(opt)

    def run(self, name=None):
        opt = self._parse_args(name)
        Duplicates(
            opt['DIRECTORY'],
            verbose=opt['--verbose'],
            unix_patterns=opt['PATTERNS']
        ).run(not opt['--no-store'])

if __name__ == '__main__':
    CommandLineInterface().run()
