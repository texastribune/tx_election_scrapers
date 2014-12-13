from __future__ import unicode_literals

import unittest


from .utils import slugify, corrected
from . import utils


class correctedTest(unittest.TestCase):
    def test_it_works(self):
        utils._corrections_cache = {
            'all': {
                'a0': 'a1',
            },
            'foo': {
                'a0': 'a2',
            },
            'bar': {
                'a0': 'a3',
            },
        }
        self.assertEqual(corrected('a0'), 'a1')
        self.assertEqual(corrected('missing'), 'missing')
        self.assertEqual(corrected('a0', corrections=['foo']), 'a2')
        self.assertEqual(corrected('a0', corrections=('foo', 'bar',)), 'a3')
        # assert uses lastest slug
        self.assertEqual(
            corrected('a0', corrections=['foo', 'bar', 'xyzzy']), 'a3')
        # assert ignores nonexistent ones in general
        self.assertEqual(
            corrected('a0', corrections=['foo', 'poop', 'bar', 'xyzzy']), 'a3')

    def test_always_uses_original_slug(self):
        utils._corrections_cache = {
            'all': {
                'a0': 'a1',
            },
            'foo': {
                'a0': 'a2',
                'a1': 'b1',
            },
            'bar': {
                'a0': 'a3',
                'b1': 'c1',
            },
        }
        self.assertEqual(corrected('a0'), 'a1')
        self.assertEqual(corrected('a0', corrections=('foo', )), 'a2')
        self.assertEqual(corrected('a0', corrections=['foo', 'bar']), 'a3')


class SlugifyTest(unittest.TestCase):
    def test_it_works(self):
        self.assertEqual(slugify(''), '')
        self.assertEqual(slugify('a'), 'a')
        self.assertEqual(slugify('a b'), 'a-b')
        self.assertEqual(slugify('Ronald McDonald'), 'ronald-mcdonald')
        self.assertEqual(slugify('M.C. Chris'), 'mc-chris')
        self.assertEqual(slugify('foo', corrections=['poop']), 'foo')


if __name__ == '__main__':
    unittest.main()
