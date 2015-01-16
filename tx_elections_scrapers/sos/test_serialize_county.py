from __future__ import unicode_literals

import os
import unittest

from . import serialize_county


BASE_DIR = os.path.dirname(__file__)


class RealtimeCountyTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rc-2012_rep_runoff_senate.htm')).read()
        doc = serialize_county.document_fromstring(html_file)
        race = serialize_county.process_race(doc)
        self.assertEqual(race['type'], 'realtime')
        self.assertEqual(race['name'], 'U. S. Senator')
        self.assertEqual(race['election'], '2012 Republican Party Primary Runoff')
        self.assertEqual(race['updated_at'], '7/31/2012  9:29:44 PM')
        self.assertEqual(race['candidates'][0],
            {'name': ('Ted', 'Cruz'), 'party': 'REP'})
        self.assertEqual(len(race['candidates']), 2)
        self.assertEqual(len(race['rows']), 255)  # 254 + statewide summary


class HistoricalCountyTest(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hc-2014_special_sd28.html')).read()
        doc = serialize_county.document_fromstring(html_file)
        race = serialize_county.process_race(doc)
        self.assertEqual(race['type'], 'historical')
        self.assertEqual(race['name'], 'State Senator, District 28')
        self.assertEqual(race['election'], '2014 Special Election, Senate District 28')
        self.assertEqual(race['updated_at'], '9/9/2014')
        self.assertEqual(race['candidates'][0],
            {'name': ('Jodey', 'Arrington'), 'party': 'REP'})
        self.assertEqual(len(race['candidates']), 6)
        self.assertEqual(len(race['rows']), 52)


if __name__ == '__main__':
    unittest.main()
