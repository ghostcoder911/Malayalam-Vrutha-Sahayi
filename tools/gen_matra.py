#!/usr/bin/env python3
import re
from pathlib import Path

from xdis import load_module
from xdis.codetype.code20 import Code2


def collect_unicode(co, out):
    for c in co.co_consts:
        if isinstance(c, Code2):
            collect_unicode(c, out)
        elif type(c).__name__ == "UnicodeForPython3":
            out.append(str(c))
        elif isinstance(c, tuple):
            for t in c:
                if type(t).__name__ == "UnicodeForPython3":
                    out.append(str(t))


def main():
    root = Path(__file__).resolve().parents[1]
    co = load_module(str(root / "tools" / "matra.pyc"))[3]
    ft = [c for c in co.co_consts if isinstance(c, Code2) and c.co_name == "findCharType"][0]
    order = []
    collect_unicode(ft, order)
    order61 = order[:61]

    text = Path("/tmp/vs_extract/matra.py").read_text(encoding="utf-8")
    it = iter(range(61))

    def repl(_m):
        return repr(order61[next(it)])

    new_text = re.sub(r"u'\\u'", repl, text)
    # Drop trailing junk from decompiler
    new_text = re.sub(r"\nreturn\s*\n\s*# okay decompiling.*", "\n", new_text, flags=re.DOTALL)
    lines = new_text.splitlines()
    out_lines = []
    skip = True
    for line in lines:
        if line.startswith("from syllable import"):
            skip = False
        if skip:
            continue
        out_lines.append(line)
    hdr = "# -*- coding: utf-8 -*-\n# Ported from Vrutha Sahayi 0.1 matra.pyc\n\n"
    (root / "vruthasahayi" / "matra.py").write_text(hdr + "\n".join(out_lines) + "\n", encoding="utf-8")
    print("wrote matra.py")


if __name__ == "__main__":
    main()
