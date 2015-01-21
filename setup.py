#!/usr/bin/env python
from distutils.core import setup

setup(
    name='duplicates',
    version='1.0',
    description='Find duplicate files in a directory',
    author='Luca Lanziani',
    author_email='luca@lanziani.com',
    url='https://github.com/Nss/Duplicates',
    install_requires=['docopt', 'schema'],
    packages=['duplicates'],
    scripts=['bin/duplicates'],
)
