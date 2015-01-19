from __future__ import unicode_literals

from datetime import datetime  # I usually don't like doing this
import os
import unittest

from . import statewide, county


BASE_DIR = os.path.dirname(__file__)


class SosFunctionalTest(unittest.TestCase):
    """
    Test the convenience wrappers.

    FIXME this is just copy pasted from the integration test right now.
    """
    def test_statewide(self):
        mapping = (
            # election, reference
            ('hs-2010_general.html', (533, datetime(2010, 11, 2, 0, 0, 0))),
            ('hs-2010_rep_runoff.html', (25, datetime(2010, 4, 13, 0, 0, 0))),
            ('hs-2011_special_runoff_hd14.html', (1, datetime(2011, 12, 13,))),
            ('hs-2012_general.html', (584, datetime(2012, 11, 6, 0, 0, 0))),
            ('hs-2014_general.html', (548, datetime(2014, 11, 4, 0, 0, 0))),
            ('rs-2010_dem_primary.htm', (27, datetime(2010, 2, 17, 12, 44, 51))),
            ('rs-2010_rep_primary.htm', (97, datetime(2010, 2, 17, 12, 44, 52))),
            ('rs-2012_dem_primary.htm', (52, datetime(2012, 5, 23, 12, 56, 57))),
            ('rs-2012_rep_primary.htm', (160, datetime(2012, 5, 23, 12, 57, 0))),
            ('rs-2014_general.htm', (160, datetime(2014, 11, 10, 17, 7, 56))),
        )
        for election, reference in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = statewide(html_file)
            # print election
            num_races, updated_at = reference
            self.assertEqual(data['total_rows'], num_races)
            self.assertEqual(data['updated_at'], updated_at)

    def test_county(self):
        mapping = (
            # election, reference
            ('hc-2010_general_governor.html', (255, 5)),
            ('hc-2012_general_president.html', (255, 11)),
            ('hc-2012_rep_primary.html', (255, 8)),
            ('hc-2014_special_sd28.html', (52, 6)),
            ('rc-2012_dem_runoff_sd137.htm', (1, 2)),
            ('rc-2012_rep_runoff_rr.htm', (255, 2)),
            ('rc-2012_rep_runoff_senate.htm', (255, 2)),
            ('rc-2014_general_cd1.html', (13, 2)),
            ('rc-2014_general_gov_county.html', (255, 5)),
            ('rc-2014_general_senate.html', (255, 5)),
        )
        for election, reference in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = county(html_file)
            # print election
            num_counties, num_candidates = reference
            self.assertEqual(data['total_rows'], num_counties)
            self.assertEqual(len(data['candidates']), num_candidates)


if __name__ == '__main__':
    unittest.main()
