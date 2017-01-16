# -*- coding: utf-8 -*-

"""
Discord API Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Discord API.

:copyright: (c) 2015-2016 Rapptz
:license: MIT, see LICENSE for more details.

"""

__title__ = 'discord'
__author__ = 'Rapptz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2016 Rapptz'
__version__ = '0.14.3'

from collections import namedtuple
from .client import Client
from .user import User

VersionInfo = namedtuple('VersionInfo',
                         'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=14, micro=3, releaselevel='final',
                           serial=0)
