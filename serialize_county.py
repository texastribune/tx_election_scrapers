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


def process_race(doc):
    election = doc.xpath('//h2[2]')[0].text
    h3s = doc.xpath('//h3')
    updated_at = h3s[0].text
    race_name = h3s[1].text
    return {
        'election': election,
        'updated_at': updated_at,
        'name': race_name,
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
