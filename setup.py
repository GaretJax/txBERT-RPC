#!/usr/bin/env python

from distutils.core import setup

from txbert import __version__ as version

setup(
    name = 'txbert',
    version = version,
    description = 'Twisted BERT-RPC Library',
    author = 'Jonathan Stoppani',
    author_email = 'jonathan.stoppani@gmail.com',
    url = 'http://garetjax.info',
    packages = ['txbert'],
    license='MIT',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
