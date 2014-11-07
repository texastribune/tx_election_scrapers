import os
import unittest

import mock

import serialize


BASE_DIR = os.path.dirname(__file__)


class HistoricalStatewideSummaryTest(unittest.TestCase):
    def test_bundle_races_works(self):
        html_file = open(os.path.join(BASE_DIR, 'support/2012-general.html')).read()
        doc = serialize.document_fromstring(html_file)
        races = serialize.bundle_races(doc)
        self.assertEqual(len(races), 584)

    @unittest.skip('maybe later')
    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/2012-general.html'))
        serialize.process(fh)
        self.assertEqual(mock_out.write.call_count, 938)


@unittest.skip('maybe later')
class RealtimeStatewideSummaryTest(unittest.TestCase):
    @mock.patch('sys.stdout')
    def test_it_works(self, mock_out):
        fh = open(os.path.join(BASE_DIR, 'support/may29_160_state.htm'))
        serialize.process(fh)
        self.assertEqual(mock_out.write.call_count, 669)


if __name__ == '__main__':
    unittest.main()
