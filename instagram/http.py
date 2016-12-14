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

import aiohttp
import asyncio
import json
import sys
import logging
import inspect
import weakref
from random import randint as random_integer

from .errors import HTTPException, Forbidden, NotFound, LoginFailure, \
    GatewayNotFound
from . import utils, __version__

log = logging.getLogger(__name__)


@asyncio.coroutine
def json_or_text(response):
    text = yield from response.text(encoding='utf-8')
    if 'application/json' in response.headers['Content-Type']:
        return json.loads(text)
    return text


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Discord API."""

    BASE          = 'https://api.instagram.com'
    API_BASE      = BASE     + '/v1'
    USERS         = API_BASE + '/users'
    ME            = USERS    + '/self'
    OAUTH         = API_BASE + '/oauth'
    LOGIN         = OAUTH    + '/authorize'
    MEDIA         = API_BASE + '/media'
    TAGS          = API_BASE + '/tags'
    LOCATIONS     = API_BASE + '/locations'

    SUCCESS_LOG = '{method} {url} has received {text}'
    REQUEST_LOG = '{method} {url} with {data} has returned {status}'

    def __init__(self, connector=None, *, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.connector = connector
        self.session = aiohttp.ClientSession(connector=connector,
                                             loop=self.loop)
        self._locks = weakref.WeakValueDictionary()
        self.token = None

        user_agent = ('InstagramBot (<URL> {0})'
                      ' Python/{1[0]}.{1[1]} aiohttp/{2}')
        self.user_agent = user_agent.format(__version__, sys.version_info,
                                            aiohttp.__version__)

    @asyncio.coroutine
    def request(self, method, url, *, bucket=None, **kwargs):
        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock(loop=self.loop)
            if bucket is not None:
                self._locks[bucket] = lock

        # header creation
        headers = {
            'User-Agent': self.user_agent,
        }

        requestData = kwargs.pop('params', {})

        if self.token is not None:
            requestData['access_token'] = self.token

        kwargs['params'] = requestData
        kwargs['headers'] = headers
        with (yield from lock):
            for tries in range(5):
                r = yield from self.session.request(method, url, **kwargs)
                log.debug(self.REQUEST_LOG.format(method=method, url=url,
                                                  status=r.status,
                                                  data=requestData))
                try:
                    # even errors have text involved in them so this is safe to
                    #   call
                    data = yield from json_or_text(r)

                    # the request was successful so just return the text/json
                    if 300 > r.status >= 200:
                        log.debug(self.SUCCESS_LOG.format(method=method,
                                  url=url, text=data))
                        return data

                    # we are being rate limited
                    if r.status == 429:
                        fmt = ('We are being rate limited. Retrying in {:.2}'
                               'seconds. Handled under the bucket "{}"')

                        # sleep a bit
                        retry_after = data['retry_after'] / 1000.0
                        log.info(fmt.format(retry_after, bucket))
                        yield from asyncio.sleep(retry_after)
                        continue

                    # we've received a 502, unconditional retry
                    if r.status == 502 and tries <= 5:
                        yield from asyncio.sleep(1 + tries * 2)
                        continue

                    # the usual error cases
                    if r.status == 403:
                        raise Forbidden(r, data)
                    elif r.status == 404:
                        raise NotFound(r, data)
                    else:
                        raise HTTPException(r, data)
                finally:
                    # clean-up just in case
                    yield from r.release()

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    # state management

    @asyncio.coroutine
    def close(self):
        yield from self.session.close()

    def recreate(self):
        self.session = aiohttp.ClientSession(connector=self.connector,
                                             loop=self.loop)

    def _token(self, token):
        self.token = token
