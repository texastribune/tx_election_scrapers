from __future__ import unicode_literals

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
            ('hs-2010_general.html', '2010-11-02T00:00:00'),
            ('hs-2010_rep_runoff.html', '2010-04-13T00:00:00'),
            ('hs-2011_special_runoff_hd14.html', '2011-12-13T00:00:00'),
            ('hs-2012_general.html', '2012-11-06T00:00:00'),
            ('hs-2014_general.html', '2014-11-04T00:00:00'),
            ('rs-2010_dem_primary.htm', '2010-02-17T12:44:51'),
            ('rs-2010_rep_primary.htm', '2010-02-17T12:44:52'),
            ('rs-2012_dem_primary.htm', '2012-05-23T12:56:57'),
            ('rs-2012_rep_primary.htm', '2012-05-23T12:57:00'),
            ('rs-2014_general.htm', '2014-11-10T17:07:56'),
        )
        for election, updated_at in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = statewide(html_file)
            self.assertEqual(data['updated_at'], updated_at)

    def test_county(self):
        mapping = (
            ('hc-2010_general_governor.html', 255),
            ('hc-2012_general_president.html', 255),
            ('hc-2012_rep_primary.html', 255),
            ('hc-2014_special_sd28.html', 52),
            # ('rc-2012_dem_runoff_sd137.htm', 255),  # FIXME
            # ('rc-2012_rep_runoff_rr.htm', 255),  # FIXME
            # ('rc-2012_rep_runoff_senate.htm', 255),  # FIXME
            # ('rc-2014_general_cd1.html', 255),  # FIXME
            ('rc-2014_general_gov_county.html', 255),
            ('rc-2014_general_senate.html', 255),
        )
        for election, row_count in mapping:
            html_file = open(os.path.join(BASE_DIR, 'support', election))
            data = county(html_file)
            self.assertEqual(len(data['rows']), row_count)


if __name__ == '__main__':
    unittest.main()
