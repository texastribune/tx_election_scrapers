from __future__ import unicode_literals

import re
import unicodedata


def slugify(text):
    """
    Slugify text according to the same rules as Django's slugify.

    Reference: https://github.com/django/django/blob/stable/1.7.x/django/utils/text.py
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    return re.sub('[-\s]+', '-', text)
