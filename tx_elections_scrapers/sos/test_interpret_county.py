from __future__ import unicode_literals

import os
import unittest

from . import interpret_county
from . import serialize_county


BASE_DIR = os.path.dirname(__file__)


class RealtimeCountyTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rc-2012_rep_runoff_senate.htm')).read()
        doc = serialize_county.document_fromstring(html_file)
        results = serialize_county.process_race(doc)
        results2 = interpret_county.interpret(results)
        # assert `interpret` modifies in-place
        self.assertEqual(results, results2)


class HistoricalCountyTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hc-2014_special_sd28.html')).read()
        doc = serialize_county.document_fromstring(html_file)
        results = serialize_county.process_race(doc)
        results2 = interpret_county.interpret(results)
        # assert `interpret` modifies in-place
        self.assertEqual(results, results2)


if __name__ == '__main__':
    unittest.main()
