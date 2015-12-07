#!/usr/bin/env python
import codecs
import locale
import sys

if sys.stdout.encoding is None or sys.stdout.encoding.upper() != 'UTF-8':
    encoding = sys.stdout.encoding or locale.getpreferredencoding()
    try:
        encoder = codecs.getwriter(encoding)
    except LookupError:
        sys.stdout.write("Warning: unknown encoding %s specified in locale().\n" % encoding)
        encoder = codecs.getwriter('UTF-8')
    if encoding.upper() != 'UTF-8':
        sys.stdout.write("Warning: stdout in %s format. Diacritical signs are" +
                         " represented in XML-coded format." % encoding)
    try:
        sys.stdout = encoder(sys.stdout.buffer, 'xmlcharrefreplace')
    except AttributeError:
        sys.stdout = encoder(sys.stdout, 'xmlcharrefreplace')
if sys.stderr.encoding is None or sys.stderr.encoding.upper() != 'UTF-8':
    encoding = sys.stderr.encoding or locale.getpreferredencoding()
    try:
        encoder = codecs.getwriter(encoding)
    except LookupError:
        sys.stderr.write("Warning: unknown encoding %s specified in locale().\n" % encoding)
        encoder = codecs.getwriter('UTF-8')
    if encoding.upper() != 'UTF-8':
        sys.stderr.write("Warning: stderr in %s formaat. Diacritical signs are" +
                         " represented in XML-coded format." % encoding)
    try:
        sys.stderr = encoder(sys.stderr.buffer, 'xmlcharrefreplace')
    except AttributeError:
        sys.stderr = encoder(sys.stderr, 'xmlcharrefreplace')
