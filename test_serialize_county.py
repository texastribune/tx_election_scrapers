from __future__ import unicode_literals

import os
import unittest

import serialize_county


BASE_DIR = os.path.dirname(__file__)


class RealtimeCounty(unittest.TestCase):
    def test_it_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/july31_162_race0.htm')).read()
        doc = serialize_county.document_fromstring(html_file)
        race = serialize_county.process_race(doc)
        self.assertEqual(race['name'], 'U. S. Senator')
        self.assertEqual(race['election'], '2012 Republican Party Primary Runoff')
        self.assertEqual(race['updated_at'], '7/31/2012  9:29:44 PM')
        self.assertEqual(len(race['candidates']), 2)
        self.assertEqual(len(race['data']), 255)  # 254 + statewide summary


if __name__ == '__main__':
    unittest.main()
