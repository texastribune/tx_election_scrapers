from __future__ import unicode_literals

import unittest


from utils import slugify


class SlugifyTest(unittest.TestCase):
    def test_it_works(self):
        self.assertEqual(slugify(''), '')
        self.assertEqual(slugify('a'), 'a')
        self.assertEqual(slugify('a b'), 'a-b')
        self.assertEqual(slugify('Ronald McDonald'), 'ronald-mcdonald')
        self.assertEqual(slugify('M.C. Chris'), 'mc-chris')


if __name__ == '__main__':
    unittest.main()
