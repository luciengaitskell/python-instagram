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


class InstagramException(Exception):
    """Base exception class for instagram.py

    Ideally speaking, this could be caught to handle any exceptions thrown from
    this library.
    """
    pass


class ClientException(InstagramException):
    """Exception that's thrown when an operation in the :class:`Client` fails.

    These are usually for exceptions that happened due to user input.
    """
    pass


class HTTPException(InstagramException):
    """Exception that's thrown when an HTTP request operation fails.

    .. attribute:: response

        The response of the failed HTTP request. This is an
        instance of `aiohttp.ClientResponse`__.

        __ http://aiohttp.readthedocs.org/en/stable/client_reference.html#aiohttp.ClientResponse

    .. attribute:: text

        The text of the error. Could be an empty string.
    """

    def __init__(self, response, message):
        self.response = response
        if type(message) is dict:
            # Take 'meta' value, if it exists
            message = message.get('meta', message)
            self.text = message.get('error_message', '')
            self.code = message.get('code', 0)
        else:
            self.text = message

        fmt = '{0.reason} (status code: {0.status})'
        if len(self.text):
            fmt += ': {1}'

        super().__init__(fmt.format(self.response, self.text))


class Forbidden(HTTPException):
    """Exception that's thrown for when status code 403 occurs.

    Subclass of :exc:`HTTPException`
    """
    pass


class NotFound(HTTPException):
    """Exception that's thrown for when status code 404 occurs.

    Subclass of :exc:`HTTPException`
    """
    pass


class InvalidArgument(ClientException):
    """Exception that's thrown when an argument to a function
    is invalid some way (e.g. wrong value or wrong type).

    This could be considered the analogous of ``ValueError`` and
    ``TypeError`` except derived from :exc:`ClientException` and thus
    :exc:`InstagramException`.
    """
    pass


class LoginFailure(ClientException):
    """Exception that's thrown when the :meth:`Client.login` function
    fails to log you in from improper credentials or some other misc.
    failure.
    """
    pass
