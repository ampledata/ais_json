#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Python AIS Gateway.

:author: Daniel J. Grinkevich
:copyright: Copyright 2017 Daniel J. Grinkevich
:license: GNU General Public License, Version 3
:source: <https://github.com/ampledata/aisgw>
"""

import os
import sys

import setuptools

__title__ = 'aisgw'
__version__ = '1.0.0b2'
__author__ = 'Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__license__ = 'GNU General Public License, Version 3'  # NOQA pylint: disable=R0801


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='Python AIS JSON Gateway.',
    author='Daniel J. Grinkevich',
    author_email='oss@undef.net',
    packages=['aisgw'],
    package_data={'': ['LICENSE']},
    package_dir={'aisgw': 'aisgw'},
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    url='https://github.com/ampledata/aisgw',
    zip_safe=False,
    include_package_data=True,
    install_requires=['requests', 'libais >= 0.16'],
    entry_points={'console_scripts': ['aisgw = aisgw.cmd:cli']}
)
