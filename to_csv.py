#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | to_csv.py
  cat support/example.html | to_csv.py
"""
from __future__ import unicode_literals

from lxml.html import document_fromstring

import sys


class Bucket(list):
    """A helper for constructing list of lists one element at a time"""
    def __init__(self, *args):
        super(Bucket, self).__init__(*args)
        self.advance()

    def drip(self, o):
        """appends the object to the current mini-bucket"""
        self[-1].append(o)

    def advance(self):
        """create a new mini-bucket"""
        self.append([])

    def soft_advance(self):
        """create a new mini-bucket only if there's something new"""
        if self[-1]:
            self.advance()


def bundle_races(doc):
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

    for race in races:
        print race[0].text_content()

    return races


if __name__ == '__main__':
    html_file = sys.stdin.read()
    doc = document_fromstring(html_file)
    races = bundle_races(doc)
