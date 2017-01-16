# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-2016 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
from . import __version__ as library_version
from .http import create_client_session
from .user import User


class Client:
    """Allows for usage and handling of multiple 'User' objects."""

    def __init__(self, *, loop=None):
        self.users = []
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = create_client_session()

    @asyncio.coroutine
    def add_user(self, *args, token=None, **kwargs):
        """Add a 'User' object to the 'Client' object.

        If a token is passed as a keyword argument, the token of the 'User'
        object is checked and set.
        """
        user = User(self.session, *args, loop=self.loop, **kwargs)

        print("Token: " + token)
        if (token is not None):
            yield from user.static_login(token)
        self.users.append(user)
        return user

    @asyncio.coroutine
    def close(self):
        """Close the 'aiohttp.ClientSession' object."""
        yield from self.session.close()
