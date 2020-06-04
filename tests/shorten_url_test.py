from argparse import ArgumentError
import unittest
import sys
import shorten_url


class ShortenURLTest(unittest.TestCase):
    
    def test_parse_options_open_no_arg(self):
        sys.argv[1:] = ['--open']
        with self.assertRaises(SystemExit) as ex:
            self.assertRaises(ArgumentError, shorten_url.parse_options())
        
        self.assertEqual(ex.exception.code, 2)

    def test_parse_options_open_arg(self):
        url = 'https://www.google.com'
        temp_args = sys.argv
        sys.argv[1:] = ['--open', url]
        args = shorten_url.parse_options()
        sys.argv = temp_args

        self.assertEqual(args.open, url)
        self.assertEqual(args.shorten, None)

    def test_parse_options_shorten_no_arg(self):
        sys.argv.append('--shorten')
        with self.assertRaises(SystemExit) as ex:
            self.assertRaises(ArgumentError, shorten_url.parse_options())
        
        self.assertEqual(ex.exception.code, 2)

    def test_parse_options_shorten_arg(self):
        url = 'https://www.google.com'
        temp_args = sys.argv
        sys.argv[1:] = ['--shorten', url]
        args = shorten_url.parse_options()
        sys.argv = temp_args

        self.assertEqual(args.open, None)
        self.assertEqual(args.shorten, url)

    def test_parse_options_no_args(self):
        temp_args = sys.argv
        sys.argv = [sys.argv[0]]
        args = shorten_url.parse_options()
        sys.argv = temp_args

        self.assertEqual(args.open, None)
        self.assertEqual(args.shorten, None)

    def test_parse_options_open_and_shorten(self):
        url = 'https://www.google.com'
        temp_args = sys.argv
        sys.argv[1:] = ['--open', url, '--shorten', url]
        
        with self.assertRaises(RuntimeError):
            shorten_url.parse_options()
        sys.argv = temp_args

