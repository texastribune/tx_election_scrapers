from __future__ import unicode_literals

import os
import unittest

from . import interpret_statewide
from . import serialize_statewide


BASE_DIR = os.path.dirname(__file__)


class RealtimeTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2014_general.htm'))
        data = serialize_statewide.serialize(html_file)
        # sanity check
        self.assertEqual(data['total_rows'], 160)
        self.assertEqual(data['election'], '2014 General Election')

        data2 = interpret_statewide.interpret(data)
        # assert modifies in-place
        self.assertEqual(data, data2)


class HistoricalTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hs-2012_general.html'))
        data = serialize_statewide.serialize(html_file)
        # sanity check
        self.assertEqual(data['total_rows'], 584)
        self.assertEqual(data['election'], '2012 General Election')

        data2 = interpret_statewide.interpret(data)
        # assert modifies in-place
        self.assertEqual(data, data2)


if __name__ == '__main__':
    unittest.main()
