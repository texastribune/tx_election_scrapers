from __future__ import unicode_literals

import datetime
import os
import re
import unicodedata

import yaml


# config
CORRECTIONS_DIR = 'corrections'


_corrections_cache = {}


def corrected(slug, corrections=None):
    """
    Pull the corrected version of `slug` from `corrections`.

    Corrections should be in increasing specificity. Each correction should
    correspond to a .yml file in the ./corrections directory that contains the
    slug corrections.
    """
    # global _corrections_cache  # implied because {} is mutable

    if corrections is None:
        lookups = ['all']
    else:
        lookups = ['all'] + list(corrections)
    for lookup in lookups:
        if lookup not in _corrections_cache:
            # WISHLIST lookup can also be a file handle
            try:
                path = '{}.yml'.format(os.path.join(CORRECTIONS_DIR, lookup))
                _corrections_cache[lookup] = yaml.load(open(path, 'rb'))
            except IOError:  # no slugifyuch file
                _corrections_cache[lookup] = {}
    new_slug = slug
    for lookup in lookups:
        new_slug = _corrections_cache[lookup].get(slug, new_slug)
    return new_slug


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


def slugify(text, corrections=None):
    """
    Slugify text according to the same rules as Django's slugify.

    Reference: https://github.com/django/django/blob/stable/1.7.x/django/utils/text.py
    """
    try:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    except TypeError:  # `text` was not unicode to begin with
        pass
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    slug = re.sub('[-\s]+', '-', text)
    return corrected(slug, corrections)


def int_ish(numeric_maybe):
    """
    HACK quick fix for getting empty things instead of a numeric string

    >>> int_ish('')
    None
    >>> int_ish('0')
    0
    >>> int_ish('1337')
    1337
    >>> int_ish('1,337')
    1337
    """
    if numeric_maybe == '':
        return None
    return int(numeric_maybe.replace(',', ''))


def dthandler(obj):
    """
    JSON handler for datetime objects.

    http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript/2680060#2680060
    """
    return obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
