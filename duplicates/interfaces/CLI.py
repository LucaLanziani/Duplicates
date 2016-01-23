#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os
import pprint
import sys

from docopt import docopt
from duplicates import start_logger
from duplicates.analyzer import Analyzer
from duplicates.indexer import Indexer
from duplicates.libraries.output import ConsoleOutput
from duplicates.libraries.utils import DuplicateExceptions
from schema import And, Optional, Or, Schema, SchemaError


log = logging.getLogger(__name__)


class CommandLineInterface(object):
    """Usage: %(name)s [options] DIRECTORY [PATTERNS...]

    You can filter the analysed files passing multiple patterns through command
    line, the patterns can include "Unix shell-style wildcards"

    Options:
        --index                     index directory content
        --show-indexed              print all the files in the index
        --duplicates                print files that have duplicates, duplicates path are printed in TSV format
        --progress                  print progress update in console
        --no-store                  do not save the gathered information on filesystem
        --intersection=<DIRECTORY>  show the common files between the two directories
        --difference=<DIRECTORY>    show the files in the current dir that are not in the given dir
        --log-level=<LEVEL>         process debug level [default: CRITICAL]

    Examples:
        %(name)s .                  # every file
        %(name)s . '*.png'          # only .png files
        %(name)s . '*.png' '*.jpg'  # .png and .jpg files
    """

    def __init__(self):
        super(CommandLineInterface, self).__init__()
        self.output = ConsoleOutput(True, False)

    def _validate_args(self, opt):
        schema = Schema({
            'DIRECTORY': And(os.path.exists, error="Dir does not exists"),
            Optional('--index'): bool,
            Optional('--show-indexed'): bool,
            Optional('--duplicates'): bool,
            Optional('--progress'): bool,
            Optional('--no-store'): bool,
            Optional('--intersection'): Or(unicode, str, None),
            Optional('--difference'): Or(unicode, str, None),
            Optional('--log-level'): Or(unicode, str),
            Optional('PATTERNS'): [Or(unicode, str)]
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

    def _create_index(self, opt):
        Indexer(
            opt['DIRECTORY'],
            output=ConsoleOutput(False, opt['--progress']),
            unix_patterns=opt['PATTERNS']
        ).run(not opt['--no-store'])

    def _analize(self, opt):
        analyzer = Analyzer(opt['DIRECTORY'], output=ConsoleOutput(True, False))
        if opt['--intersection']:
            analyzer.intersection(opt['--intersection'])
        if opt['--difference']:
            analyzer.difference(opt['--difference'])
        if opt['--duplicates']:
            for duplicates in analyzer.duplicates():
                self.output.print("\t".join(duplicates))
        if opt['--show-indexed']:
            analyzer.show_indexed()


    def run(self, name=None):
        try:
            opt = self._parse_args(name)
            start_logger(opt['--log-level'])

            if opt['--index']:
                self._create_index(opt)

            if opt['--intersection'] or opt['--difference'] or opt['--duplicates'] or opt['--show-indexed']:
                self._analize(opt)

        except KeyboardInterrupt:
            log.exception('Exiting on CTRL^C')
        except DuplicateExceptions as e:
            log.critical('Something when wrong with the software: %s', e.message)
            if hasattr(e, 'exit_code'):
                sys.exit(e.exit_code)
            sys.exit(os.EX_SOFTWARE)

if __name__ == '__main__':
    CommandLineInterface().run()
