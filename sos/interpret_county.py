#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  ./interpret_county.py [options]

Options:
  --slugify  Slugify politician names

Interprets and transforms results from stdin to make it easier for other
scripts to consume.

Expects JSON from serialize_county.py.

Examples:
  cat support/july31_162_race0_county.htm | ./serialize_county.py | ./interpret_county.py
  cat support/2014_special_sd28_county.html | ./serialize_county.py | ./interpret_county.py
"""
from __future__ import unicode_literals

import json
import sys

from pprint import pprint
from docopt import docopt

from fips import FIPS


INT_FIELDS = [
    'precincts_reported',
    'precincts_total',
    'provisional_ballots',
    'provisional_ballots_early',
    'registered_voters',
    'total_votes',
    'total_votes_early',
]


def coerce_types(obj):
    """Modifies dict in-place to coerce values."""
    for k, v in obj.items():
        if v == 'N/A':
            obj[k] = None
        elif k in INT_FIELDS:
            obj[k] = int(v.replace(',', ''))


def coerce_votes(obj):
    """Modifies dict in-place to coerce values."""
    return {k: int(v.replace(',', '')) for k, v in obj.items()}


if __name__ == '__main__':
    arguments = docopt(__doc__)
    data = json.load(sys.stdin)
    for result in data['data']:
        voting_results = result.pop('results')
        results_early = result.pop('results_early', None)
        coerce_types(result)
        result['results'] = coerce_votes(voting_results)
        if results_early is not None:
            result['results_early'] = coerce_votes(results_early)

        # new data
        fips_key = result['name'].replace(' ', '')
        if fips_key in FIPS:
            result['fips'] = FIPS[fips_key]
        else:
            result['fips'] = None
        pprint(result)
