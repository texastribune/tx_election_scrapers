#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | ./serialize_county.py
  cat support/example.html | ./serialize_county.py
"""
from __future__ import unicode_literals

import json
import sys

from lxml.html import document_fromstring


def groupby_by_two(iterable):
    """
    chunk iterable into groups of two.

    >>> groupby_by_two([1, 2, 3, 4, 5])
    ((1, 2), (3, 4))
    """
    return zip(iterable[::2], iterable[1::2])


def county_to_cells(county):
    """
    Take county... two TRs, and make it two lists of TDs/THs.
    """
    return [x.getchildren() for x in county]


def process_county_historical(county, candidates):
    data = county.getchildren()
    county_name = data[0].text_content()
    results = {}
    for idx, candidate in enumerate(candidates, start=1):
        results[candidate] = data[idx].text_content()

    return {
        'name': county_name,
        'total_votes': data[-3].text_content(),
        'registered_voters': data[-2].text_content(),
        'turnout': data[-1].text_content(),
        'results': results,
    }


def process_county_realtime(county, candidates):
    data = county_to_cells(county)
    name = data[0][0].text_content()
    results = {}
    early_results = {}
    for idx, candidate in enumerate(candidates, start=1):
        results[candidate] = data[0][idx].text
        early_results[candidate] = data[1][idx].text

    return {
        'name': name,
        'total_votes': data[0][-6].text,
        'total_votes_early': data[1][-6].text,
        'registered_voters': data[0][-5].text,
        'turnout': data[0][-4].text,
        'provisional_ballots': data[0][-3].text,
        'provisional_ballots_early': data[1][-3].text,
        'precincts_reported': data[0][-2].text,
        'precincts_total': data[0][-1].text,
        'results': results,
        'results_early': results,
    }


def process_race(doc):
    h2s = doc.xpath('//h2')
    h3s = doc.xpath('//h3')
    rows = doc.xpath('//tr')

    # metadata
    election = h2s[1].text
    updated_at = h3s[0].text
    try:
        race_name = h3s[1].text
        is_historical = False
    except IndexError:
        race_name = ''.join(doc.xpath('//form/text()')).strip()
        is_historical = True

    row_one = [x.text for x in rows[0].getchildren()]
    # first column that's not '...' counting from the right
    extra_cols = [x == '...' for x in reversed(row_one)].index(False)

    # candidates
    first_names = row_one[1:-extra_cols]  # non-surname
    surnames = [x.text for x in rows[1].getchildren()[1:-extra_cols]]
    parties = [x.text for x in rows[2].getchildren()[1:-extra_cols]]
    candidates = [{'name': x[:2], 'party': x[2]} for x in zip(first_names, surnames, parties)]
    candidates_names = [' '.join(x) for x in zip(first_names, surnames)]

    # group rows by two for each "county"
    county_data = []
    if is_historical:
        for county in rows[3:]:
            county_data.append(process_county_historical(county, candidates_names))
    else:
        for county in groupby_by_two(rows[3:]):
            county_data.append(process_county_realtime(county, candidates_names))

    return {
        'election': election,
        'updated_at': updated_at,
        'name': race_name,
        'candidates': candidates,
        'rows': county_data,
        'total_rows': len(county_data),
        'type': 'historical' if is_historical else 'realtime',
    }


def serialize(fh):
    """Take a file-like object or text and serialize it."""
    if hasattr(fh, 'read'):
        html_file = fh.read()
    else:
        html_file = fh
    doc = document_fromstring(html_file)
    return process_race(doc)


def main():
    data = serialize(sys.stdin)
    # TODO process `--indent` option
    json.dump(data, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
