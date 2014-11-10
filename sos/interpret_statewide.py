#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
  cat support/example.html | ./serialize_statewide.py | ./interpret_statewide.py

Interprets and transforms results to make it easier for other scripts to
consume.

Expects JSON from serialize_statewide.py.

Sample usage:
  cat support/2010_general.html | ./serialize_statewide.py | ./interpret_statewide.py
  cat support/2012_general.html | ./serialize_statewide.py | ./interpret_statewide.py
"""
from __future__ import unicode_literals

import json
import sys

from pprint import pprint


def coerce_types(obj):
    """Modifies dict in-place to coerce values."""
    for k, v in obj.items():
        if v == 'N/A':
            obj[k] = None
        elif k in INT_FIELDS:
            obj[k] = int(v.replace(',', ''))


def coerce_votes(obj):
    """Modifies dict in-place to coerce values."""
    return {k: int(v.replace(',', '')) for k, v in obj.items()}


if __name__ == '__main__':
    data = json.load(sys.stdin)
    for race in data:
        coerce_types(race['metadata'])
        pprint(race)
