# -*- coding: utf-8 -*-
"""Integration tests using Malayalam ślokas from Akshara Sloka Sadass (2005/02)."""

from pathlib import Path
import os
import sys
import unittest

_ROOT = Path(__file__).resolve().parents[1]
_FIX = _ROOT / "fixtures" / "aksharaslokam_2005_02"

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from vruthasahayi.findvrutham import findVrutham
from vruthasahayi.matra import getMatraArray


def _fixture_files():
    if not _FIX.is_dir():
        return []
    return sorted(p for p in _FIX.glob("sloka_*.txt") if p.is_file())


class TestAksharaslokamFixtures(unittest.TestCase):
    def test_all_fixtures_parse_without_error(self):
        paths = _fixture_files()
        self.assertGreaterEqual(
            len(paths),
            1,
            "Expected sloka_*.txt under fixtures/aksharaslokam_2005_02/",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8").strip()
            self.assertGreater(len(text), 10, msg=path.name)
            gl_array, _syl = getMatraArray(text)
            joined = "".join(x for x in gl_array if x in ("v", "-", "c"))
            self.assertGreater(len(joined), 0, msg=f"{path.name}: empty gl sequence")
            rows = findVrutham(gl_array)
            self.assertGreater(len(rows), 0, msg=path.name)

    def test_sample_line_has_pattern_chars(self):
        p = _FIX / "sloka_190_udurajamukhi_jagannatha.txt"
        if not p.is_file():
            self.skipTest("fixture missing")
        text = p.read_text(encoding="utf-8")
        gl, _ = getMatraArray(text)
        s = "".join(gl)
        self.assertIn("v", s)
        self.assertIn("|", s)


if __name__ == "__main__":
    unittest.main()
