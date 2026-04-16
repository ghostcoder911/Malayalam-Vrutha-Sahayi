# -*- coding: utf-8 -*-
"""Regression tests for Malayalam syllable segmentation (findSyllable FSA)."""

import os
import sys
import unittest

# Package root: vruthasahayi-web/
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from vruthasahayi.matra import getMatraArray
from vruthasahayi.syllable import findSyllable, getCharClass


def iter_syllables(text):
    prev = 0
    n = len(text)
    while prev < n:
        end = findSyllable(text, prev, n)
        yield text[prev:end]
        prev = end


class TestFindSyllable(unittest.TestCase):
    def test_kavithayude_five_syllables_not_one(self):
        word = "കവിതയുടെ"
        parts = list(iter_syllables(word))
        self.assertEqual(
            parts,
            ["ക", "വി", "ത", "യു", "ടെ"],
            "FSA must return early on -1 transitions; whole-word span caused always-guru / ശ്രീ",
        )

    def test_matra_array_not_single_guru_for_word(self):
        word = "കവിതയുടെ"
        gl, _ = getMatraArray(word)
        joined = "".join(x for x in gl if x in ("v", "-", "c"))
        self.assertNotEqual(joined, "-")
        self.assertGreaterEqual(len(joined), 2)

    def test_char_class_table_bounds(self):
        # U+0D00 can be _xx (0); consonants like ക must classify for the FSA.
        self.assertEqual(getCharClass("\u0d00"), 0)
        self.assertNotEqual(getCharClass("ക"), 0)
        # Past U+0D6F the original table does not apply; treat as class 0.
        self.assertEqual(getCharClass(chr(0x0D70)), 0)
        for o in range(0x0D00, 0x0D70):
            getCharClass(chr(o))


if __name__ == "__main__":
    unittest.main()
