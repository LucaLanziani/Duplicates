#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os
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
        --purge                     purge store from no more existent files
        --show-indexed              print all the files in the index
        --duplicates                print multiple copies of the same file in TSV format
        --progress                  print progress update in console
        --no-store                  do not save the gathered information on filesystem
        --intersection=<DIRECTORY>  show the common files between the two directories
        --difference=<NEWDIR>       show the files in NEWDIR that are not in DIRECTORY
        --find=<file>               find same files in DIRECTORY
        --log-level=<LEVEL>         process debug level [default: INFO]

    Examples:
        %(name)s .                  # uses the filters in the store
        %(name)s . '*'              # every file
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
            Optional('--purge'): bool,
            Optional('--show-indexed'): bool,
            Optional('--duplicates'): bool,
            Optional('--progress'): bool,
            Optional('--no-store'): bool,
            Optional('--find'): Or(unicode, str, None),
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

    def _on_index(self, opt):
        indexer = Indexer(
            opt['DIRECTORY'],
            output=ConsoleOutput(False, opt['--progress']),
            unix_patterns=opt['PATTERNS']
        )

        if opt['--purge']:
            indexer.purge().save()

        if opt['--index']:
            indexer.run(not opt['--no-store'])

    def _analyze(self, opt):
        index1 = Indexer(
            opt['DIRECTORY'],
            unix_patterns=opt['PATTERNS']
        )
        log.warning('Last update on index was %s' % index1.last_update)
        log.warning('if you want an updated result add --index option')
        analyzer = Analyzer(output=ConsoleOutput(True, False))

        if opt['--intersection']:
            index2 = Indexer(
                opt['--intersection'],
                unix_patterns=index1.filters
            ).index()
            results = analyzer.intersection(index1, index2)
            for tuple in results:
                self.output.print("%s -> %s" % (tuple[0], tuple[1]))

        if opt['--difference']:
            index2 = Indexer(
                opt['--difference'],
                unix_patterns=index1.filters
            ).index()
            results = analyzer.difference(index1, index2)
            self.output.print("%s" % '\n'.join(results))

        if opt['--find']:
            results = index1.find(opt['--find'])
            if results:
                self.output.print("%s" % '\n'.join(results))
            else:
                self.output.print('File not found')

        if opt['--duplicates']:
            for duplicates in analyzer.duplicates(index1):
                self.output.print("\t".join(duplicates))

    def run(self, name=None):
        try:
            opt = self._parse_args(name)
            start_logger(opt['--log-level'])

            if opt['--index'] or opt['--purge']:
                self._on_index(opt)

            if opt['--intersection'] or opt['--difference'] or opt['--duplicates'] or opt['--find']:
                self._analyze(opt)

        except KeyboardInterrupt:
            log.exception('Exiting on CTRL^C')
        except DuplicateExceptions as e:
            log.critical('Something when wrong with the software: %s', e.message)
            if hasattr(e, 'exit_code'):
                sys.exit(e.exit_code)
            sys.exit(os.EX_SOFTWARE)

if __name__ == '__main__':
    CommandLineInterface().run()
