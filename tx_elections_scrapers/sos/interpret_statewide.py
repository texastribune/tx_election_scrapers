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
  cat support/hs-2014_general.html | ./serialize_statewide.py | ./interpret_statewide.py
  cat support/rs-2014_general.htm | ./serialize_statewide.py | ./interpret_statewide.py
"""
from __future__ import unicode_literals

import json
import re
import sys

from dateutil.parser import parse
from docopt import docopt
from tx_elections_scrapers.sos.utils import int_ish, slugify, dthandler


INCUMBENT_PATTERN = re.compile(r'\s(\-\s|\()Incumbent\)?|\(I\)$')
PARTY_SLUGS = ('republican', 'democratic')  # slurrrrmmmm


def interpret(data):
    """
    Interpret the raw serialized data in-place.
    """
    data['slug'] = slugify(data['election'])
    rows = data['rows']

    if data['type'] == 'realtime':
        result_keys = ['name', 'party', 'votes_early', 'percent_early', 'votes', 'percent']
        date_string = data['updated_at'].rsplit('\u00a0', 2)[1]
        data['updated_at'] = parse(date_string)
        check_presidential = True
    else:
        result_keys = ('name', 'party', 'votes', 'percent')
        date_string = data['updated_at']
        data['updated_at'] = parse(date_string)
        check_presidential = False
    # Find party if this is a primary. Based on the template the SoS uses, it's
    # the second word.
    party = data['election'].split()[1].lower()
    data['party'] = party if party in PARTY_SLUGS else None
    for race in rows:
        race['slug'] = slugify(race['name'], corrections=[data['slug']])
        header = race.pop('header')
        # modify result_keys to support presidential races
        if check_presidential:
            # replace 'party' with 'delegates'
            result_keys[1] = 'delegates' if 'DELEGATES' in header else 'party'
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
            if 'delegates' in candidate_result:
                candidate_result['delegates'] = int_ish(candidate_result['delegates'])
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
    json.dump(data, sys.stdout, indent=indent_amount, default=dthandler)


if __name__ == '__main__':
    main()
