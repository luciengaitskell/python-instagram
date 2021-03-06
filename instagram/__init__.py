"""
Instagram API Wrapper.

~~~~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Instagram API.

:copyright: (c) 2016-2017 Lucien Gaitskell
:license: MIT, see LICENSE for more details.
"""

__title__ = 'instagram'
__author__ = 'Lucien Gaitskell'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016-2017 Lucien Gaitskell'
__version__ = '0.4.1'

from collections import namedtuple
from .client import Client
from .user import User
from .errors import *

VersionInfo = namedtuple('VersionInfo',
                         'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=4, micro=1,
                           releaselevel='development', serial=0)
