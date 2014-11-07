#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | ./serialize.py
  cat support/example.html | ./serialize.py
"""
from __future__ import unicode_literals

from lxml.html import document_fromstring
import codecs
import cStringIO
import csv
import json
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


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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


def process_race(race):
    """Extract meaning from a collection of TR elements about a race."""
    race_name = race[0].text_content()
    tabular_data = []
    meta_data = []
    in_meta = False
    for row in race[1:]:
        cells = row.getchildren()
        datum = [x.text.strip() for x in cells if x is not None and x.text]
        if in_meta:
            meta_data.append(datum)
            continue
        if '----' in datum[0]:
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


def process(fh):
    html_file = fh.read()
    doc = document_fromstring(html_file)
    races = bundle_races(doc)
    results = []
    for race in races:
        results.append(process_race(race))
    output_races(results)


if __name__ == '__main__':
    process(sys.stdin)
