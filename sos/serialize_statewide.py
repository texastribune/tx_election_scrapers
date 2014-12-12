#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | ./serialize_statewide.py
  cat support/example.html | ./serialize_statewide.py
"""
from __future__ import unicode_literals

import json
import sys

from lxml.html import document_fromstring

from utils import Bucket


def bundle_races(doc):
    """Group TR elements by race."""
    rows = doc.xpath('.//tr')

    # Separate the rows into sets of rows for each race.
    races = Bucket()
    for row in rows:
        if row.xpath('.//th'):
            # skip headers
            continue
        elif row.xpath('.//td[1]/text()[contains(., "----")]'):
            # separator encountered
            races.advance()
        else:
            races.drip(row)

    return races


def get_meta(doc):
    h2s = doc.xpath('//h2')
    h3s = doc.xpath('//h3')
    election = h2s[1].text
    updated_at = h3s[-1].text
    return {
        'election': election,
        'updated_at': updated_at,
        'type': 'realtime' if ':' in updated_at else 'historical',
    }


def process_race(race):
    """Extract meaning from a collection of TR elements about a race."""
    race_name = race[0].text_content()
    tabular_data = []
    meta_data = []
    in_meta = False
    for row in race[1:]:
        cells = row.getchildren()
        datum = [x.text_content().strip() for x in cells[1:]]
        if in_meta:
            meta_data.append(datum[1:])  # has an extra padding TD
            continue
        if '----' in ''.join(datum):
            in_meta = True
            continue
        tabular_data.append(datum)
    return {
        'name': race_name,
        'data': tabular_data,
        'metadata': meta_data,
    }


def output_races(races):
    # TODO indent amount from command line
    json.dump(races, sys.stdout, indent=2)
    # writer = UnicodeWriter(sys.stdout)


def process(fh, outputter=output_races):
    html_file = fh.read()
    doc = document_fromstring(html_file)
    races = bundle_races(doc)
    results = []
    for race in races:
        results.append(process_race(race))
    data = get_meta(doc)
    data['total_rows'] = len(results)
    data['rows'] = results
    outputter(data)
    return data


if __name__ == '__main__':
    process(sys.stdin)
