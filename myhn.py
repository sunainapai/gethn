#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2019 Sunaina Pai
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""MyHN - Get my Hacker News submissions."""


__version__ = '0.0.1-dev1'
__author__ = 'Sunaina Pai'
__credits__ = ('Hacker News community for great content and exposing '
               'the content via REST API.')


import argparse
import json
import os
import urllib
import urllib.request

_BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
_USER_URL = _BASE_URL + 'user/{}.json'
_ITEM_URL = _BASE_URL + 'item/{}.json'


def _parse_cli():
    """Parse command line arguments.

    Return:
        argparse.Namespace: Parsed arguments.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='Hacker News username')
    parser.add_argument('-l', '--limit', type=int, default=0,
                        help='limit the number of items to pull')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {version}'
                        .format(version=__version__))
    args = parser.parse_args()
    return args


def _write_json(filename, data):
    """Write ``data`` to ``filename`` in JSON format.

    Arguments:
        filename (str): Path to file to write data to.
        data (dict): Data to write.
    """
    path = os.path.expanduser(filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def get_item_ids(user):
    """Get item IDs for ``user``.

    Arguments:
        user (str): Hacker News username.

    Return:
        list: List of IDs of items submitted by ``user``.

    """
    user_url = _USER_URL.format(user)
    response = urllib.request.urlopen(user_url).read()
    user_info = json.loads(response.decode('utf-8'))
    item_ids = user_info.get('submitted')
    return item_ids


def get_item(item_id):
    """Get item data for ``item_id``.

    Arguments:
        item_id (int): Hacker News item ID.

    Return:
        dict: Dictionary object that represents item data.
            ``item_id``.
    """
    item_url = _ITEM_URL.format(item_id)
    response = urllib.request.urlopen(item_url).read()
    item = json.loads(response.decode('utf-8'))
    return item


def get_items(user, limit=0):
    """Get items for ``user``.

    Arguments:
        user (str): Hacker News username.

    Return:
        dict: Dictionary object that contains item IDs as keys with item
            data as their values.

    """
    item_ids = get_item_ids(user)
    items = {}
    for count, item_id in enumerate(item_ids):
        if limit == count > 0:
            break
        item = get_item(item_id)
        items[item_id] = item
    return items


def main():
    """Start MyHN."""
    args = _parse_cli()
    items = get_items(args.user, args.limit)
    _write_json('~/.myhn.json', items)


if __name__ == '__main__':
    main()
