# -*- coding: utf-8 -*-
import os
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from vruthasahayi import data
from vruthasahayi.nearest_vrutham import nearest_catalog_matches


class TestNearest(unittest.TestCase):
    def test_exact_pattern_returns_empty(self):
        k = next(iter(data.vruthamDict))
        self.assertEqual(nearest_catalog_matches(k), [])

    def test_unknown_line_gets_ranked_neighbors(self):
        p = "vvvvvv-vv-vvvvvvvvvvvvvv--"
        self.assertNotIn(p, data.vruthamDict)
        hits = nearest_catalog_matches(p, top_k=3, min_ratio=0.75)
        self.assertGreaterEqual(len(hits), 1)
        self.assertIn("similarity", hits[0])
        self.assertIn("lineVruthamNameMl", hits[0])
        self.assertIn("catalogPattern", hits[0])


if __name__ == "__main__":
    unittest.main()
