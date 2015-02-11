from __future__ import unicode_literals

import datetime
import os
import unittest

from . import interpret_statewide
from . import serialize_statewide


BASE_DIR = os.path.dirname(__file__)


class RealtimeTest(unittest.TestCase):
    def test_it_works_2014_general(self):
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2014_general.htm'))
        data = serialize_statewide.serialize(html_file)
        # sanity check
        self.assertEqual(data['total_rows'], 160)
        self.assertEqual(data['election'], '2014 General Election')

        data2 = interpret_statewide.interpret(data)
        # assert modifies in-place
        self.assertEqual(data, data2)

    def test_it_works_2012_rep_primary(self):
        """
        Presidential year.
        """
        html_file = open(os.path.join(BASE_DIR, 'support/rs-2012_rep_primary.htm'))
        data = serialize_statewide.serialize(html_file)
        # sanity check
        self.assertEqual(data['total_rows'], 160)
        self.assertEqual(data['election'], '2012 Republican Party Primary Election')

        data = interpret_statewide.interpret(data)  # XXX data = f(data) is evil
        race_result = data['rows'][0]  # president result
        self.assertNotIn('header', race_result)
        self.assertEqual(race_result['data'][0]['name'], 'Michele Bachmann')
        self.assertEqual(race_result['data'][0]['delegates'], 0)
        # assert this candidate is missing party info
        self.assertNotIn('party', race_result['data'][0])

        race_result = data['rows'][1]  # non-president result
        self.assertNotIn('header', race_result)
        self.assertEqual(race_result['data'][0]['name'], 'Glenn Addison')
        self.assertEqual(race_result['data'][0]['party'], 'REP')
        # assert this candidate is missing delegate info
        self.assertNotIn('delegates', race_result['data'][0])


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


class ParsingTest(unittest.TestCase):
    def test_updated_at(self):
        mapping = (
            # only do one since the integration test does the rest
            # ('hs-2010_general.html', '2010-11-02T00:00:00'),
            # ('hs-2010_rep_runoff.html', '2010-04-13T00:00:00'),
            # ('hs-2011_special_runoff_hd14.html', '2011-12-13T00:00:00'),
            # ('hs-2012_general.html', '2012-11-06T00:00:00'),
            ('hs-2014_general.html', datetime.datetime(2014, 11, 4)),
            # ('rs-2010_dem_primary.htm', '2010-02-17T12:44:51'),
            # ('rs-2010_rep_primary.htm', '2010-02-17T12:44:52'),
            # ('rs-2012_dem_primary.htm', '2012-05-23T12:56:57'),
            # ('rs-2012_rep_primary.htm', '2012-05-23T12:57:00'),
            ('rs-2014_general.htm', datetime.datetime(2014, 11, 10, 17, 7, 56)),
        )
        for election, updated_at in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = interpret_statewide.interpret(serialize_statewide.serialize(html_file))
            self.assertEqual(data['updated_at'], updated_at)

    def test_party_works(self):
        mapping = (
            ('hs-2010_general.html', None),
            ('hs-2010_rep_runoff.html', 'republican'),
            ('hs-2011_special_runoff_hd14.html', None),
            ('hs-2012_general.html', None),
            ('hs-2014_general.html', None),
            ('rs-2010_dem_primary.htm', 'democratic'),
            ('rs-2010_rep_primary.htm', 'republican'),
            ('rs-2012_dem_primary.htm', 'democratic'),
            ('rs-2012_rep_primary.htm', 'republican'),
            ('rs-2014_general.htm', None),
        )
        for election, party in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = interpret_statewide.interpret(serialize_statewide.serialize(html_file))
            self.assertEqual(data['party'], party)


if __name__ == '__main__':
    unittest.main()
