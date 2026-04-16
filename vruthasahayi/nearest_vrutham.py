# -*- coding: utf-8 -*-
"""
Best-effort nearest meters when no exact vruthamDict key matches.

The original engine only recognizes lines whose laghu/guru string equals a key
in data.vruthamDict (classical fixed patterns). Modern or free lines rarely hit
exactly; we rank catalog patterns by similarity so the UI can show likely names.
"""

from __future__ import annotations

import difflib
from typing import Any, List, Optional

from . import data


def nearest_catalog_matches(
    pattern: str,
    top_k: int = 5,
    min_ratio: float = 0.52,
    max_len_delta: Optional[int] = None,
) -> List[Any]:
    """
    Return up to ``top_k`` catalog meters whose stored patterns are most similar
    to ``pattern`` (v / - / c symbols).

    ``min_ratio`` is difflib.SequenceMatcher ratio (0–1). Per-id, the best-matching
    dict key is kept when the same meter id appears under several patterns.
    """
    if not pattern or pattern in data.vruthamDict:
        return []

    plen = len(pattern)
    if max_len_delta is None:
        max_len_delta = max(8, plen // 3)

    best_by_id: dict[int, tuple[float, str]] = {}
    for key, vid in data.vruthamDict.items():
        if not key:
            continue
        if abs(len(key) - plen) > max_len_delta:
            continue
        ratio = difflib.SequenceMatcher(a=pattern, b=key).ratio()
        if ratio < min_ratio:
            continue
        prev = best_by_id.get(vid)
        if prev is None or ratio > prev[0]:
            best_by_id[vid] = (ratio, key)

    out = []
    for vid, (ratio, key) in best_by_id.items():
        if 0 <= vid < len(data.vruthamTable):
            name_ml = data.vruthamTable[vid][1]
        else:
            name_ml = ""
        out.append(
            {
                "vruthamId": vid,
                "lineVruthamNameMl": name_ml,
                "catalogPattern": key,
                "similarity": round(ratio, 4),
            }
        )

    out.sort(key=lambda x: -x["similarity"])
    return out[:top_k]
