#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  curl ... | to_csv.py
  cat support/example.html | to_csv.py
"""
from __future__ import unicode_literals

from lxml.html import document_fromstring
import codecs
import cStringIO
import csv

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
    race_name = race[0].text_content()
    results = []
    for rows in race[1:-2]:  # we don't care about the last two rows
        result = [race_name]
        result.extend([x.text.strip() for x in rows.getchildren()[1:]])
        results.append(result)
    return results


def output_races(races):
    writer = UnicodeWriter(sys.stdout)
    for race in races:
        writer.writerow(race)


if __name__ == '__main__':
    html_file = sys.stdin.read()
    doc = document_fromstring(html_file)
    races = bundle_races(doc)
    results = []
    for race in races:
        results.extend(process_race(race))
    output_races(results)
