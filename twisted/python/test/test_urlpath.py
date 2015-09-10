# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{twisted.python.urlpath}.
"""

from twisted.trial import unittest
from twisted.python import urlpath


class _BaseURLPathTests(object):
    def test_strReturnsStr(self):
        """
        Calling C{str()} with a L{URLPath} will always return a L{str}.
        """
        self.assertEqual(type(self.path.__str__()), str)

    def test_stringConversion(self):
        """
        Calling C{str()} with a L{URLPath} will return the same URL that it was
        constructed with.
        """
        self.assertEqual(str(self.path),
                         "http://example.com/foo/bar?yes=no&no=yes#footer")

    def test_childString(self):
        """
        Calling C{str()} with a C{URLPath.child()} will return a URL which is
        the child of the URL it was instantiated with.
        """
        self.assertEqual(str(self.path.child(b'hello')),
                         "http://example.com/foo/bar/hello")
        self.assertEqual(str(self.path.child(b'hello').child(b'')),
                         "http://example.com/foo/bar/hello/")

    def test_siblingString(self):
        """
        Calling C{str()} with a C{URLPath.sibling()} will return a URL which is
        the sibling of the URL it was instantiated with.
        """
        self.assertEqual(str(self.path.sibling(b'baz')),
                         'http://example.com/foo/baz')

        # The sibling of http://example.com/foo/bar/
        #     is http://example.comf/foo/bar/baz
        # because really we are constructing a sibling of
        # http://example.com/foo/bar/index.html
        self.assertEqual(str(self.path.child(b'').sibling(b'baz')),
                         'http://example.com/foo/bar/baz')

    def test_parentString(self):
        """
        Calling C{str()} with a C{URLPath.parent()} will return a URL which is
        the parent of the URL it was instantiated with.
        """
        # parent should be equivalent to '..'
        # 'foo' is the current directory, '/' is the parent directory
        self.assertEqual(str(self.path.parent()),
                         'http://example.com/')
        self.assertEqual(str(self.path.child(b'').parent()),
                         'http://example.com/foo/')
        self.assertEqual(str(self.path.child(b'baz').parent()),
                         'http://example.com/foo/')
        self.assertEqual(str(self.path.parent().parent().parent().parent().parent()),
                         'http://example.com/')

    def test_hereString(self):
        """
        Calling C{str()} with a C{URLPath.here()} will return a URL which is
        the URL that it was instantiated with, without any file, query, or
        fragment.
        """
        # here should be equivalent to '.'
        self.assertEqual(str(self.path.here()), 'http://example.com/foo/')
        self.assertEqual(str(self.path.child(b'').here()),
                         'http://example.com/foo/bar/')



class BytesURLPathTests(_BaseURLPathTests, unittest.TestCase):
    """
    Tests for interacting with a L{URLPath} created with C{fromBytes}.
    """
    def setUp(self):
        self.path = urlpath.URLPath.fromBytes(
            b"http://example.com/foo/bar?yes=no&no=yes#footer")


    def test_mustBeBytes(self):
        """
        C{URLPath.fromBytes} must take a L{bytes} argument.
        """
        with self.assertRaises(ValueError):
            urlpath.URLPath.fromBytes("a str")



class StringURLPathTests(_BaseURLPathTests, unittest.TestCase):
    """
    Tests for interacting with a L{URLPath} created with C{fromString}.
    """
    def setUp(self):
        self.path = urlpath.URLPath.fromString(
            "http://example.com/foo/bar?yes=no&no=yes#footer")


    def test_mustBeStr(self):
        """
        C{URLPath.fromString} must take a L{string} argument.
        """
        with self.assertRaises(ValueError):
            urlpath.URLPath.fromString(b"a bytes")
