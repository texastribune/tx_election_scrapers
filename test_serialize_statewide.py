from __future__ import unicode_literals

import os
import unittest

import mock

import serialize_statewide


BASE_DIR = os.path.dirname(__file__)


class HistoricalStatewideSummaryTest(unittest.TestCase):
    def test_bundle_races_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/2012-general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        self.assertEqual(len(races), 584)

    def test_process_races_works_historical(self):
        html_file = open(os.path.join(BASE_DIR, 'support/2012-general.html')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['name'], 'President/Vice-President')
        self.assertEqual(len(race['data']), 11)
        self.assertEqual(len(race['metadata']), 1)

    def test_process_races_works_realtime(self):
        html_file = open(os.path.join(BASE_DIR, 'support/may29_160_state.htm')).read()
        doc = serialize_statewide.document_fromstring(html_file)
        races = serialize_statewide.bundle_races(doc)
        race = serialize_statewide.process_race(races[0])
        self.assertEqual(race['name'], 'President/Vice-President')
        self.assertEqual(len(race['data']), 9)
        self.assertEqual(len(race['metadata']), 5)

    @unittest.skip('maybe later')
    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/2012-general.html'))
        serialize_statewide.process(fh)
        self.assertEqual(mock_out.write.call_count, 938)


@unittest.skip('maybe later')
class RealtimeStatewideSummaryTest(unittest.TestCase):
    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/may29_160_state.htm'))
        serialize_statewide.process(fh)
        self.assertEqual(mock_out.write.call_count, 669)


if __name__ == '__main__':
    unittest.main()
