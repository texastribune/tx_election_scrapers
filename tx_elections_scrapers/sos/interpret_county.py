#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  ./interpret_county.py [options]

Options:
  --indent=<n>  Indent JSON

Interprets and transforms results from stdin to make it easier for other
scripts to consume. What this does:

* shows FIPS for each county
* cleans numeric values to be numbers
* normalizes missing data to `null` value
* (optional) Show candidate names as computer friendly slugs

Expects JSON from serialize_county.py.

Examples:
  cat support/july31_162_race0_county.htm | ./serialize_county.py | ./interpret_county.py
  cat support/2014_special_sd28_county.html | ./serialize_county.py | ./interpret_county.py
  curl -X POST --data "election=2014+Republican+Party+Primary+Election&lboRace=U.+S.+Senator" \
    http://elections.sos.state.tx.us/elchist.exe | ./serialize_county.py | \
    ./interpret_county.py --indent=2
"""
from __future__ import unicode_literals

import json
import sys

from docopt import docopt

from tx_elections_scrapers.sos.fips import FIPS
from tx_elections_scrapers.sos.utils import slugify, int_ish


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
        if v == 'N/A' or v is None:
            obj[k] = None
        elif k in INT_FIELDS:
            obj[k] = int(v.replace(',', ''))


def coerce_votes(obj, corrections_lookup):
    """Changes CSV-like dict to a list of results and coerce values."""
    new_results = []
    for name, count in obj.items():
        new_results.append({
            'name': name,
            'slug': slugify(name, corrections=corrections_lookup),
            'votes': int_ish(count)
        })
    new_results.sort(key=lambda x: x['votes'], reverse=True)
    return new_results


def interpret(data):
    """Modify `data` in place according to `options`."""
    data['election_slug'] = slugify(data['election'])
    corrections_lookup = (data['election_slug'], )
    data['slug'] = slugify(data['name'], corrections=corrections_lookup)
    # interpret data['candidates']
    for candidate in data['candidates']:
        # modify in place
        candidate['slug'] = slugify(' '.join(candidate['name']), corrections=corrections_lookup)

    # interpret data['rows']
    for row in data['rows']:
        voting_results = row.pop('results')
        results_early = row.pop('results_early', None)
        coerce_types(row)
        row['results'] = coerce_votes(voting_results, corrections_lookup)
        if results_early is not None:
            row['results_early'] = coerce_votes(results_early, corrections_lookup)

        # new data
        fips_key = row['name'].replace(' ', '')
        if fips_key in FIPS:
            row['fips'] = FIPS[fips_key]
        else:
            row['fips'] = None
    return data


def main():
    options = docopt(__doc__)

    data = json.load(sys.stdin)
    interpret(data)

    # output
    indent_amount = options['--indent'] and int(options['--indent'])
    json.dump(data, sys.stdout, indent=indent_amount)


if __name__ == '__main__':
    main()
