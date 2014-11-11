#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  ./interpret_county.py [options]

Options:
  --slugify     Slugify candidate names
  --indent=<n>  Indent JSON

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

from docopt import docopt

from fips import FIPS
from utils import slugify


make_slugs = False


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


def interpret(data):
    """Modify `data` in place according to `options`."""
    # interpret data['candidates']
    for candidate in data['candidates']:
        # modify in place, always set a slug irregardless of `make_slugs`
        candidate['slug'] = slugify(' '.join(candidate['name']))

    # interpret data['rows']
    for row in data['rows']:
        voting_results = row.pop('results')
        results_early = row.pop('results_early', None)
        coerce_types(row)
        row['results'] = coerce_votes(voting_results, make_slugs)
        if results_early is not None:
            row['results_early'] = coerce_votes(results_early, make_slugs)

        # new data
        fips_key = row['name'].replace(' ', '')
        if fips_key in FIPS:
            row['fips'] = FIPS[fips_key]
        else:
            row['fips'] = None
    return data


def main():
    global make_slugs  # XXX evil
    options = docopt(__doc__)
    make_slugs = options['--slugify']

    data = json.load(sys.stdin)
    interpret(data)

    # output
    indent_amount = options['--indent'] and int(options['--indent'])
    json.dump(data, sys.stdout, indent=indent_amount)


if __name__ == '__main__':
    main()
