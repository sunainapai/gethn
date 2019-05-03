"""Tests for MyHN."""

import unittest
from unittest import mock

import myhn


class MyHNTest(unittest.TestCase):
    """Tests for MyHN."""

    @mock.patch('urllib.request.urlopen')
    def test_get_item_ids(self, mock_urlopen):
        mock_urlopen().read.return_value = b'{"submitted": [1, 2, 3]}'
        item_ids = myhn.get_item_ids(None)
        self.assertEqual(item_ids, [1, 2, 3])

    @mock.patch('urllib.request.urlopen')
    def test_get_item(self, mock_urlopen):
        mock_urlopen().read.return_value = b'{"foo": "bar"}'
        item = myhn.get_item(None)
        self.assertEqual(item, {"foo": "bar"})

    @mock.patch('urllib.request.urlopen')
    def test_get_items(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None)
        self.assertEqual(items[1], {"foo": "bar"})
        self.assertEqual(items[2], {"foo": "bar"})
        self.assertEqual(items[3], {"foo": "bar"})
