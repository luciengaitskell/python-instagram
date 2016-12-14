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
import inspect
from .http import HTTPClient


def _func_():
    # emulate __func__ from C++
    return inspect.currentframe().f_back.f_code.co_name


class User:
    """Interaction of an Instagram user.

    Attributes
    -----------
    client : HTTPClient
        The object to communicate to the Instagram API through.
    """

    def __init__(self, *args, **kwargs):
        self.client = HTTPClient(*args, **kwargs)

    # Login management:
    @asyncio.coroutine
    def static_login(self, token):
        old_token = self.client.token
        self.client._token(token)

        try:
            data = yield from self.client.get(self.client.ME)
        except HTTPException as e:
            self.client._token(old_token)
            if e.response.status == 401:
                raise LoginFailure('Improper token has been passed.') from e
            raise e

        return data

    @asyncio.coroutine
    def close(self):
        yield from self.client.close()

    ''' API INTERACTION: '''

    # User:
    def get_user(self, user_id):
        """Get a user's information."""
        return self.client.get(self.client.USERS + '/{}'.format(user_id),
                               bucket=_func_())

    def get_self(self):
        """Get this user's information."""
        return self.client.get_user('self')

    def get_user_recent_media(self, user_id):
        """Get this user's information.

        Parameters
        -----------
        user_id : str
            The message to check if you're mentioned in.
        """
        return self.client.get(self.client.USERS +
                               '/{}/media/recent'.format(user_id),
                               bucket=_func_())

    def get_self_recent_media(self):
        """Get this user's recent media."""
        return self.get_user_recent_media('self')

    def get_self_liked_media(self):
        """Get this user's recent liked media."""
        return self.client.get(self.client.ME + '/media/liked', bucket=_func_())

    def search_users(self, query):
        """Search for users based on query.

        Parameters
        -----------
        query : str
            The user search query.
        """
        params = {
                'q': query,
        }
        return self.client.get(self.client.USERS + '/search', params=params,
                               bucket=_func_())

    # Relationships:
    def get_self_follows(self):
        """Get this user's followed users."""
        url = self.client.ME + '/follows'
        return self.client.get(url, bucket=_func_())

    def get_self_followed_by(self):
        """Get this user's followers."""
        url = self.client.ME + '/followed-by'
        return self.client.get(url, bucket=_func_())

    def get_self_requested_by(self):
        """Get this user's requested followers."""
        url = self.client.ME + '/requested-by'
        return self.client.get(url, bucket=_func_())

    def get_user_relationship(self, user_id):
        """Get a user's relationship to this user.

        Parameters
        -----------
        user_id : str
            The user to check the relationship of.
        """
        url = self.client.USERS + '/{}/relationship'.format(user_id)
        return self.client.get(url, bucket=_func_())

    def set_user_relationship(self, user_id, action):
        """Set a user's relationship to this user.

        Parameters
        -----------
        user_id : str
            The user to change the relationship of.
        action : str
            The action to change the relationship. It should be one of these
            three:
                *: follow
                *: unfollow
                *: approve
                *: ignore
        """
        params = {
                'action': action
        }
        url = self.client.USERS + '/{}/relationship'.format(user_id)
        return self.client.post(url, params=params, bucket=_func_())

    # Other Media:
    def get_media(self, *, media_id=None, shortcode=None):
        """Get media by 'media_id' or 'shortcode'. Either 'media_id' or
        'shortcode' have to be inputted.

        Parameters
        -----------
        media_id (kwarg) : str (optional: None)
            The id of the media to get.
        shortcode (kwarg) : str (optional: None)
            The shortcode of the media to get.
        """
        if media_id is not None:
            url = self.client.MEDIA + '/{}'.format(media_id)
        else:
            url = self.client.MEDIA + '/shortcode/{}'.format(shortcode)

        return self.client.get(url, bucket=_func_())

    def search_media(self, *, lat, lng, distance=None):
        url = self.client.MEDIA + '/search'
        params = {
                'lat': lat,
                'lng': lng
        }
        if distance is not None:
            params['distance'] = distance

        return self.client.get(url, params=params, bucket=_func_())

    # Comments:
    def get_comments(self, media_id):
        url = self.client.MEDIA + '/{}/comments'.format(media_id)
        return self.client.get(url, bucket=_func_())

    def add_comment(self, media_id, comment):
        url = self.client.MEDIA + '/{}/comments'.format(media_id)
        params = {
                'text': comment
        }
        return self.client.post(url, params=params, bucket=_func_())

    def del_comment(self, media_id, comment_id):
        url = self.client.MEDIA + '/{}/comments/{}'.format(media_id,
                                                           comment_id)
        return self.client.get(url, bucket=_func_())

    # Likes:
    def get_likes(self, media_id):
        url = self.client.MEDIA + '/{}/likes'.format(media_id)
        return self.client.get(url, bucket=_func_())

    def add_like(self, media_id):
        url = self.client.MEDIA + '/{}/likes'.format(media_id)
        return self.client.post(url, bucket=_func_())

    def del_like(self, media_id):
        url = self.client.MEDIA + '/{}/likes'.format(media_id)
        return self.client.delete(url, bucket=_func_())

    # Tags:
    def get_tag(self, tag_name):
        url = self.client.TAGS + '/{}'.format(tag_name)
        return self.client.get(url, bucket=_func_())

    def get_tagged_media(self, tag_name):
        url = self.client.TAGS + '/{}/media/recent'.format(tag_name)
        return self.client.get(url, bucket=_func_())

    def search_tags(self, query):
        url = self.client.TAGS + '/search'
        params = {
                'q': query
        }
        return self.client.get(url, params=params, bucket=_func_())

    # Locations:
    def get_location(self, location_id):
        url = self.client.LOCATIONS + '/{}'.format(location_id)
        return self.client.get(url, bucket=_func_())

    def get_location_media(self, location_id):
        url = self.client.LOCATIONS + '/{}/media/recent'.format(location_id)
        return self.client.get(url, bucket=_func_())

    def search_locations(self, query):
        url = self.client.LOCATIONS + '/search'
        params = {
                'q': query
        }
        return self.client.get(url, params=params, bucket=_func_())
