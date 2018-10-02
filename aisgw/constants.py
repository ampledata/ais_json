#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python AIS Gateway Constants."""

import logging
import os

__author__ = 'Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__license__ = 'GNU General Public License, Version 3'  # NOQA pylint: disable=R0801


if bool(os.environ.get('DEBUG')):
    LOG_LEVEL = logging.DEBUG
    logging.debug('Debugging Enabled via DEBUG Environment Variable.')
else:
    LOG_LEVEL = logging.INFO

LOG_FORMAT = logging.Formatter(
    ('%(asctime)s aisgw %(levelname)s %(name)s.%(funcName)s:%(lineno)d - '
     '%(message)s'))

DEFAULT_PORT = 5050
DEFAULT_HOST = '0.0.0.0'

DEFAULT_URL = 'http://aprs.fi/jsonais/post'
