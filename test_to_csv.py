import os
import unittest

import mock

import to_csv


BASE_DIR = os.path.dirname(__file__)


class HistoricalStatewideSummaryTest(unittest.TestCase):
    def test_bundle_races_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/2012-general.html')).read()
        doc = to_csv.document_fromstring(html_file)
        races = to_csv.bundle_races(doc)
        self.assertEqual(len(races), 584)

    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/2012-general.html'))
        to_csv.process(fh)
        self.assertEqual(mock_out.write.call_count, 938)


class RealtimeStatewideSummaryTest(unittest.TestCase):
    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/may29_160_state.htm'))
        to_csv.process(fh)
        self.assertEqual(mock_out.write.call_count, 669)


if __name__ == '__main__':
    unittest.main()
