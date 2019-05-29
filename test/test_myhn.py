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
    def test_get_items_no_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None, {})
        self.assertEqual(items[1], {"foo": "bar"})
        self.assertEqual(items[2], {"foo": "bar"})
        self.assertEqual(items[3], {"foo": "bar"})
        self.assertEqual(len(items), 3)

    @mock.patch('urllib.request.urlopen')
    def test_get_items_with_cache(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        user_cache = {}
        user_cache[1] = {"foo": "bar old"}
        items = myhn.get_items(None, user_cache)
        self.assertEqual(items[1], {"foo": "bar old"})
        self.assertEqual(len(items), 3)

    @mock.patch('urllib.request.urlopen')
    def test_get_items_limit(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        items = myhn.get_items(None, {}, 2)
        self.assertEqual(len(items), 2)

    @mock.patch('sys.argv', ['', '', '-c', 'non-existent.json'])
    @mock.patch('urllib.request.urlopen')
    def test_main(self, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        m = mock.mock_open(read_data='{}')
        with mock.patch('builtins.open', m):
            myhn.main()
        m().write.assert_called_with(mock.ANY)

    @mock.patch('sys.argv', ['', '', '-c', 'non-existent.json'])
    @mock.patch('urllib.request.urlopen')
    @mock.patch('os.path.exists')
    def test_main_read_cache(self, mock_path_exists, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        mock_path_exists.return_value = True
        m = mock.mock_open(read_data='{}')
        with mock.patch('builtins.open', m):
            myhn.main()
        m().read.assert_called_with()
        m().write.assert_called_with(mock.ANY)

    @mock.patch('sys.argv', ['', '', '-c', 'non-existent.json'])
    @mock.patch('urllib.request.urlopen')
    @mock.patch('os.path.exists')
    def test_main_no_cache(self, mock_path_exists, mock_urlopen):
        mock_urlopen().read.side_effect = [
            b'{"submitted": [1, 2, 3]}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
            b'{"foo": "bar"}',
        ]
        mock_path_exists.return_value = False
        m = mock.mock_open(read_data='{}')
        with mock.patch('builtins.open', m):
            myhn.main()
        m().write.assert_called_with(mock.ANY)
