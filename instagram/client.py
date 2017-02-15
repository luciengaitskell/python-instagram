# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2016-2017 Lucien Gaitskell

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
from .http import create_client_session
from .user import User


class Client:
    """Allows for usage and handling of multiple 'User' objects."""

    def __init__(self, *, loop=None, client_id=None, client_secret=None,
                 redirect_uri=None):
        self.users = {}
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = create_client_session()

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @asyncio.coroutine
    def get_user(self, *args, token=None, code=None, **kwargs):
        """Add a 'User' object to the 'Client' object.

        If a token is passed as a keyword argument, the token of the 'User'
        object is checked and set.
        """
        user = User(self.session, *args, loop=self.loop, **kwargs)

        if code is not None:
            if (None in [self.client_id, self.client_secret,
                         self.redirect_uri]):
                raise ValueError("Not all client values set. Please make sure"
                                 + "'client_id', 'client_secret', and"
                                 + "'redirect_uri' have been set.")

            token = yield from user.set_token_from_code(self.client_id,
                                                        self.client_secret,
                                                        self.redirect_uri,
                                                        code)

        elif token is not None:
            yield from user.set_token(token)

        return user

    @asyncio.coroutine
    def add_user(self, *args, **kwargs):
        user = yield from self.get_user(*args, **kwargs)
        if user._id is None:
            raise ValueError(
                    "Please supply either a 'token' or 'code' argument")

        self.users[user._id] = user

        return user

    @asyncio.coroutine
    def close(self):
        """Close the 'aiohttp.ClientSession' object."""
        yield from self.session.close()
