#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | ./serialize_county.py
  cat support/example.html | ./serialize_county.py
"""
from __future__ import unicode_literals

from lxml.html import document_fromstring
import json
import sys


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
    name = data[0].text_content()
    results = {}
    for idx, candidate in enumerate(candidates, start=1):
        results[candidate] = data[idx].text_content()

    return {
        'name': name,
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
        'early_results': results,
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

    # candidates
    first_names = [x.text for x in rows[0].getchildren()[1:-6]]  # non-surname
    surnames = [x.text for x in rows[1].getchildren()[1:-6]]
    # TODO get party in rows[2]
    candidates_names_split = zip(first_names, surnames)
    candidates_names = [' '.join(x) for x in candidates_names_split]

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
        'candidates': candidates_names_split,
        'data': county_data,
    }


def output_races(races):
    # TODO indent amount from command line
    json.dump(races, sys.stdout, indent=2)
    # writer = UnicodeWriter(sys.stdout)


def process(fh):
    html_file = fh.read()
    doc = document_fromstring(html_file)
    results = process_race(doc)
    output_races(results)


if __name__ == '__main__':
    process(sys.stdin)
