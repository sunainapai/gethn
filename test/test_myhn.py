"""Tests for MyHN."""

import json
import os
import unittest
from unittest import mock

import myhn


class MyHNTest(unittest.TestCase):
    """Tests for MyHN."""

    def tearDown(self):
        if os.path.exists('cache.json'):
            os.remove('cache.json')

        if os.path.exists('no_cache.json'):
            os.remove('no_cache.json')

    @mock.patch('urllib.request.urlopen')
    def test_get_item_ids(self, mock_urlopen):
        mock_urlopen().read.return_value = b'{"submitted": [1, 2, 3]}'
        item_ids = myhn.get_item_ids(None)
        self.assertEqual(item_ids, [1, 2, 3])

    @mock.patch('urllib.request.urlopen')
    def test_get_item(self, mock_urlopen):
        mock_urlopen().read.return_value = b'{"foo": "bar"}'
        item = myhn.get_item(None)
        self.assertEqual(item, {'foo': 'bar'})

    @mock.patch('urllib.request.urlopen')
    def test_get_items_empty_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None, {})
        self.assertEqual(items, {
            1: {'foo': 'bar'},
            2: {'foo': 'bar'},
            3: {'foo': 'bar'},
        })

    @mock.patch('urllib.request.urlopen')
    def test_get_items_no_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None)
        self.assertEqual(items, {
            1: {'foo': 'bar'},
            2: {'foo': 'bar'},
            3: {'foo': 'bar'},
        })

    @mock.patch('urllib.request.urlopen')
    def test_get_items_with_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        user_cache = {
            1: {'foo': 'bar old'}
        }
        items = myhn.get_items(None, user_cache)
        self.assertEqual(items, {
            1: {'foo': 'bar old'},
            2: {'foo': 'bar'},
            3: {'foo': 'bar'},
        })

    @mock.patch('urllib.request.urlopen')
    def test_get_items_limit_with_no_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None, None, 2)
        self.assertEqual(items, {
            1: {'foo': 'bar'},
            2: {'foo': 'bar'},
        })

    @mock.patch('urllib.request.urlopen')
    def test_get_items_limit_with_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        user_cache = {
            1: {'foo': 'bar old'},
            2: {'foo': 'bar old'},
            3: {'foo': 'bar old'},
        }
        items = myhn.get_items(None, user_cache, 2)
        self.assertEqual(items, {
            1: {'foo': 'bar old'},
            2: {'foo': 'bar old'},
            3: {'foo': 'bar old'},
        })

    @mock.patch('sys.argv', ['', 'test_user', '-c', 'no_cache.json'])
    @mock.patch('urllib.request.urlopen')
    def test_main_no_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        myhn.main()

        with open('no_cache.json') as f:
            cache = json.load(f)

        self.assertEqual(cache, {
            'test_user': {
                '1': {'foo': 'bar'},
                '2': {'foo': 'bar'},
                '3': {'foo': 'bar'},
            }
        })

    @mock.patch('sys.argv', ['', 'test_user', '-c', 'cache.json'])
    @mock.patch('urllib.request.urlopen')
    def test_main_read_cache(self, mock_urlopen):
        cache = {
            'test_user': {
                '1': {'foo': 'bar old'}
            },
            'extra_user': {
                '100': {'foo': 'bar old'}
            }
        }

        with open('cache.json', 'w') as f:
            json.dump(cache, f, indent=2)

        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]

        myhn.main()

        with open('cache.json') as f:
            cache = json.load(f)

        self.assertEqual(cache, {
            'test_user': {
                '1': {'foo': 'bar old'},
                '2': {'foo': 'bar'},
                '3': {'foo': 'bar'},
            },
            'extra_user': {
                '100': {'foo': 'bar old'}
            }
        })
