from __future__ import unicode_literals

import re
import unicodedata


def slugify(text):
    """
    Slugify text according to the same rules as Django's slugify.

    Reference: https://github.com/django/django/blob/stable/1.7.x/django/utils/text.py
    """
    try:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    except TypeError:  # `text` was not unicode to begin with
        pass
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    return re.sub('[-\s]+', '-', text)


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
