import os
import glob
import unittest
from six import with_metaclass

from straceviewer.parser import strace_parser


class ParseTestCaseMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test(filename):
            def test(self):
                with open(filename) as f:
                    parsed = strace_parser.parse(f.read())
                    self.assertTrue(parsed)
            return test

        for filename in glob.glob(
            os.path.join(
                os.path.dirname(__file__),
                "testcases", "*", "*")):
            test_name = "test %s" % filename
            dict[test_name] = gen_test(filename)
        return type.__new__(mcs, name, bases, dict)


class ParseTestCase(
        with_metaclass(ParseTestCaseMeta, unittest.TestCase)):
    """Just check the tests cases can all be parsed.
    """
