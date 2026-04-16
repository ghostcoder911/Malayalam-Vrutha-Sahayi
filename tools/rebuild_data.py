#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild vruthasahayi/data.py from data.pyc + uncompyle6 stub (see /tmp/vs_extract/data.py)."""
import re
import sys
import zipfile
from pathlib import Path

from xdis import load_module


def ufix(c):
    if type(c).__name__ == "UnicodeForPython3":
        return str(c)
    return c


def load_consts(pyc_path: Path):
    _, _, _, co, *_ = load_module(str(pyc_path))
    return co.co_consts


def build_ganam(C):
    lines = ["ganamDict = {"]
    for i in range(8):
        lines.append(f"    {C[2 * i + 1]!r}: {ufix(C[2 * i])!r},")
    # laghu / guru single-matra keys (same order as original data.pyc)
    lines.append(f"    {C[17]!r}: {ufix(C[16])!r},")
    lines.append(f"    {C[19]!r}: {ufix(C[18])!r},")
    lines.append("}")
    return "\n".join(lines)


def build_vrutham_table(C, decomp_text: str):
    m = re.search(r"vruthamTable = \[(.*)\]\n\ndef vruthamNameList", decomp_text, re.DOTALL)
    if not m:
        raise ValueError("vruthamTable block not found")
    chunk = m.group(1)
    pat = re.compile(
        r"\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]"
    )
    rows = []
    for mo in pat.finditer(chunk):
        idxs = [int(mo.group(i)) for i in range(1, 7)]
        rows.append(tuple(ufix(C[j]) for j in idxs))
    lines = ["vruthamTable = ["]
    for r in rows:
        lines.append(" [")
        lines.append(
            "  {}, {}, {}, {}, {}, {}],".format(
                repr(r[0]), repr(r[1]), repr(r[2]), repr(r[3]), repr(r[4]), repr(r[5])
            )
        )
    lines.append("]")
    return "\n".join(lines), len(rows)


def main():
    here = Path(__file__).resolve().parent
    root = here.parent
    libzip = root.parent / "library.zip"
    stub = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/vs_extract/data.py")

    if not stub.is_file():
        print("Need decompiled data.py at", stub, file=sys.stderr)
        sys.exit(1)

    if libzip.is_file():
        zf = zipfile.ZipFile(libzip)
        zf.extract("data.pyc", root / "tools")
        pyc_path = root / "tools" / "data.pyc"
    else:
        pyc_path = root / "tools" / "data.pyc"
        if not pyc_path.is_file():
            print("Place data.pyc in tools/ or ensure library.zip exists", file=sys.stderr)
            sys.exit(1)

    C = load_consts(pyc_path)
    decomp = stub.read_text(encoding="utf-8", errors="replace")

    ganam = build_ganam(C)
    vtable, nrows = build_vrutham_table(C, decomp)
    print("vrutham rows:", nrows, file=sys.stderr)

    idx = decomp.find("vruthamDict")
    if idx < 0:
        raise ValueError("vruthamDict not found")
    head_g = decomp[:idx]
    gi = head_g.find("ganamDict")
    if gi < 0:
        raise ValueError("ganamDict not found in stub")
    old_ganam = head_g[gi:]
    decomp = decomp[:gi] + ganam + "\n" + decomp[idx:]

    m2 = re.search(
        r"vruthamTable = \[.*?\]\n(?=\ndef vruthamNameList)", decomp, re.DOTALL
    )
    if not m2:
        raise ValueError("vruthamTable not found in stub")

    out = decomp.replace(m2.group(0), vtable + "\n")

    # Drop decompiler footer
    out = re.sub(r"\nreturn\s*\n\s*# okay decompiling.*\Z", "\n", out, flags=re.DOTALL)

    # GUI labels in the stub are corrupted; keep only about* metadata used for credits.
    out = re.sub(
        r"\ncheckLabel =.*?\nyathiRequiredLabel =.*?\n",
        "\n",
        out,
        flags=re.DOTALL,
    )

    dest = root / "vruthasahayi" / "data.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        "# -*- coding: utf-8 -*-\n"
        "# Rebuilt from Vrutha Sahayi 0.1 data.pyc + stub.\n\n" + out,
        encoding="utf-8",
    )
    print("Wrote", dest)


if __name__ == "__main__":
    main()
