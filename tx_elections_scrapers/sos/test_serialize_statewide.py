from __future__ import unicode_literals

import os
import unittest

from . import serialize_statewide


BASE_DIR = os.path.dirname(__file__)


class StatewideSummaryTest(unittest.TestCase):
    def test_bundle_races_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hs-2012_general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        self.assertEqual(len(races), 584)

    def test_get_meta_works_historical(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hs-2012_general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        meta = serialize_statewide.get_meta(doc)
        self.assertEqual(meta['type'], 'historical')
        self.assertEqual(meta['election'], '2012 General Election')
        self.assertIn('11/6/2012', meta['updated_at'])

    def test_get_meta_works_realtime(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2012_rep_primary.htm')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        meta = serialize_statewide.get_meta(doc)
        self.assertEqual(meta['type'], 'realtime')
        self.assertEqual(meta['election'], '2012 Republican Party Primary Election')
        self.assertIn('5/23/2012  12:57:00 PM', meta['updated_at'])

    def test_process_races_works_historical(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hs-2012_general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['name'], 'President/Vice-President')
        # assert the first race gets headers
        self.assertEqual(race['header'], ['RACE', 'NAME', 'PARTY', 'CANVASS VOTES', 'PERCENT'])
        self.assertEqual(len(race['data']), 11)
        self.assertEqual(len(race['metadata']), 1)
        self.assertEqual(race['metadata'][0], ['Race Total', '7,993,851', ''])

        race = serialize_statewide.process_race(races[1])
        # assert subsequent race get no header
        self.assertEqual(race['header'], None)
        self.assertEqual(race['data'][0][0], 'Ted Cruz')

    def test_process_races_works_realtime(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2012_rep_primary.htm')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['name'], 'President/Vice-President')
        self.assertEqual(race['header'], ['RACE', 'NAME', '', 'DELEGATES',
            'EARLY VOTES', 'PERCENT', 'TOTAL VOTES', 'PERCENT'])
        self.assertEqual(len(race['data']), 9)
        self.assertEqual(len(race['metadata']), 5)
        self.assertEqual(race['metadata'][0], ['Race Total', '', '0', '', '0', ''])

    def test_process_races_finds_party_historical(self):
        html_file = open(os.path.join(BASE_DIR, 'support/hs-2012_general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)

        # President
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['data'][0], ['Mitt Romney/ Paul Ryan', 'REP', '4,569,843', '57.16%'])
        self.assertEqual(race['data'][-1], ['Rocky Anderson/ Luis J. Rodriguez', 'W-I', '426', '0.00%'])

        # CD-1
        race = serialize_statewide.process_race(races[2])
        self.assertEqual(race['data'][0], ['Louie Gohmert(I)', 'REP', '178,322', '71.42%'])
        self.assertEqual(race['data'][-1], ['Clark Patterson', 'LIB', '4,114', '1.64%'])

        # Criminal District Attorney Grayson County
        race = serialize_statewide.process_race(races[-1])
        self.assertEqual(race['data'][-1], ['Joe Brown(I)', 'REP', '32,160', '100.00%'])

    def test_process_races_finds_party_realtime(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2014_general.htm')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)

        # U. S. Senator
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['data'][0], ['John Cornyn - Incumbent', 'REP',
            '1,537,396', '61.16%', '2,855,068', '61.55%'])
        self.assertEqual(race['data'][-1], ['Mohammed Tahiro', 'W-I', '621',
            '0.02%', '1,178', '0.02%'])

        # Prop 1, no party
        race = serialize_statewide.process_race(races[-1])
        self.assertEqual(race['data'][0], ['IN FAVOR', '', '1,806,032', '81.04%',
            '3,205,867', '79.78%'])
        self.assertEqual(race['data'][-1], ['AGAINST', '', '422,338', '18.95%',
            '812,197', '20.21%'])

    def test_serialize_takes_file(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2014_general.htm'))
        data = serialize_statewide.serialize(html_file)
        self.assertEqual(data['total_rows'], 160)
        self.assertEqual(data['election'], '2014 General Election')

    def test_serialize_takes_text(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2014_general.htm'))
        data = serialize_statewide.serialize(html_file.read())
        self.assertEqual(data['total_rows'], 160)
        self.assertEqual(data['election'], '2014 General Election')

if __name__ == '__main__':
    unittest.main()
