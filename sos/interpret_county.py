#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  ./interpret_county.py [options]

Options:
  --slugify  Slugify candidate names

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
from utils import slugify


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


def coerce_votes(obj, make_slugs=False):
    """Modifies dict in-place to coerce values."""
    # this logic is kind of stupid, but it'll need to be replaced soon anyways
    # once slug transformations happen
    if make_slugs:
        return {slugify(k): int(v.replace(',', '')) for k, v in obj.items()}
    else:
        return {k: int(v.replace(',', '')) for k, v in obj.items()}


if __name__ == '__main__':
    arguments = docopt(__doc__)
    make_slugs = arguments['--slugify']
    data = json.load(sys.stdin)
    for result in data['data']:
        voting_results = result.pop('results')
        results_early = result.pop('results_early', None)
        coerce_types(result)
        result['results'] = coerce_votes(voting_results, make_slugs)
        if results_early is not None:
            result['results_early'] = coerce_votes(results_early, make_slugs)

        # new data
        fips_key = result['name'].replace(' ', '')
        if fips_key in FIPS:
            result['fips'] = FIPS[fips_key]
        else:
            result['fips'] = None
        pprint(result)
