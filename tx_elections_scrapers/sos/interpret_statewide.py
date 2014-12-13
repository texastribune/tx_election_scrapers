#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  ./interpret_statewide.py [options]

Options:
  --indent=<n>  Indent JSON

Interprets and transforms results to make it easier for other scripts to
consume.

Expects JSON from serialize_statewide.py.

Sample:
  cat support/2010_general.html | ./serialize_statewide.py | ./interpret_statewide.py
  cat support/2012_general.html | ./serialize_statewide.py | ./interpret_statewide.py
"""
from __future__ import unicode_literals

import json
import re
import sys

from docopt import docopt
from tx_elections_scrapers.sos.utils import int_ish, slugify


INCUMBENT_PATTERN = re.compile(r'\s(\-\s|\()Incumbent\)?|\(I\)$')


def interpret(data):
    data['slug'] = slugify(data['election'])
    rows = data['rows']

    if data['type'] == 'realtime':
        result_keys = ('name', 'party', 'votes_early', 'percent_early', 'votes', 'percent')
    else:
        result_keys = ('name', 'party', 'votes', 'percent')
    for race in rows:
        race['slug'] = slugify(race['name'], corrections=[data['slug']])
        new_results = []

        # candidate results
        for result in race['data']:
            candidate_result = dict(zip(result_keys, result))
            name = candidate_result['name']
            if INCUMBENT_PATTERN.search(name):
                name = INCUMBENT_PATTERN.sub('', name)
                candidate_result['name'] = name
                candidate_result['incumbent'] = True
            else:
                candidate_result['incumbent'] = False
            candidate_result['slug'] = slugify(
                candidate_result['name'], corrections=[data['slug']])
            candidate_result['votes'] = int_ish(candidate_result['votes'])
            if 'votes_early' in candidate_result:
                candidate_result['votes_early'] = int_ish(candidate_result['votes_early'])
            new_results.append(candidate_result)

        # metadata
        metadata_raw = race['metadata']
        if len(metadata_raw) == 5:
            # pprint(metadata_raw)
            metadata = {
                'votes_early': int_ish(metadata_raw[0][2]),
                'votes': int_ish(metadata_raw[0][4]),
                'provisional': int_ish(metadata_raw[1][2]),
                'provisional_early': int_ish(metadata_raw[2][4]),
                'precincts_reported': int_ish(metadata_raw[3][2]),
                'precincts_total': int_ish(metadata_raw[3][4].split(' ', 2)[0]),
                'precincts_reported_percent': metadata_raw[3][6],
                'statewide_turnout_percent': metadata_raw[4][2],
                'registered_coters': int_ish(metadata_raw[4][4].split(' ', 2)[0]),
            }
            race['metadata'] = metadata
        elif len(metadata_raw) == 2:
            metadata = {
                'votes_early': int_ish(metadata_raw[0][2]),
                'votes': int_ish(metadata_raw[0][4]),
                'precincts_reported': int_ish(metadata_raw[1][2]),
                'precincts_total': int_ish(metadata_raw[1][4].split(' ', 2)[0]),
                'precincts_reported_percent': metadata_raw[1][6],
            }
            race['metadata'] = metadata
        elif len(metadata_raw) == 1:
            metadata = {
                'votes': int_ish(metadata_raw[0][1]),
            }
            race['metadata'] = metadata

        race['data'] = new_results
    return data


def main():
    options = docopt(__doc__)
    data = json.load(sys.stdin)
    interpret(data)

    # pprint(rows)
    indent_amount = options['--indent'] and int(options['--indent'])
    json.dump(data, sys.stdout, indent=indent_amount)


if __name__ == '__main__':
    main()
