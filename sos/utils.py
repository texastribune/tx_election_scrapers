from __future__ import unicode_literals

import os
import re
import unicodedata

import yaml


# config
CORRECTIONS_DIR = 'corrections'


_corrections_cache = {}


def corrected(slug, *corrections):
    """
    Pull the corrected version of `slug` from `corrections`.

    Corrections should be in increasing specificity.
    """
    # global _corrections_cache  # implied because {} is mutable

    corrections = ['all'] + list(corrections)
    for correction in corrections:
        if correction not in _corrections_cache:
            try:
                path = '{}.yml'.format(os.path.join(CORRECTIONS_DIR, correction))
                _corrections_cache[correction] = yaml.load(open(path, 'rb'))
            except IOError:  # no slugifyuch file
                _corrections_cache[correction] = {}
    new_slug = slug
    for correction in corrections:
        new_slug = _corrections_cache[correction].get(slug, new_slug)
    return new_slug


def slugify(text, *corrections):
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
    return corrected(slug, *corrections)


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
