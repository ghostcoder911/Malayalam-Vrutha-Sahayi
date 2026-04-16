# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1 syllable.pyc (Malayalam syllable boundary + class).


def isMal(x):
    if "\u0d00" <= x <= "\u0d7f":
        return 1
    if x == "|":
        return 1
    return 0


def getCharClass(char):
    _xx = 0
    _mp = 2
    _iv = 3
    _ct = 2147483652
    _pb = _ct | 134217728
    _cn = 2147483653
    _dv = 7
    _dr = _dv | 8388608
    _dl = _dv | 67108864
    _x1 = 65536
    _x2 = 65536
    _x3 = 65536
    _s1 = _dv | _x1
    _s2 = _dv | _x2
    _s3 = _dv | _x3
    _vr = 8
    mlymCharClasses = [
        _xx,
        _xx,
        _mp,
        _mp,
        _xx,
        _iv,
        _iv,
        _iv,
        _iv,
        _iv,
        _iv,
        _iv,
        _iv,
        _xx,
        _iv,
        _iv,
        _iv,
        _xx,
        _iv,
        _iv,
        _iv,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _xx,
        _ct,
        _ct,
        _ct,
        _ct,
        _ct,
        _pb,
        _cn,
        _cn,
        _ct,
        _ct,
        _ct,
        _pb,
        _ct,
        _ct,
        _ct,
        _ct,
        _xx,
        _xx,
        _xx,
        _xx,
        _dr,
        _dr,
        _dr,
        _dr,
        _dr,
        _dr,
        _xx,
        _xx,
        _dl,
        _dl,
        _dl,
        _xx,
        _s1,
        _s2,
        _s3,
        _vr,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _dr,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _iv,
        _iv,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
        _xx,
    ]
    # Original syllable.pyc: ZWJ / ZWNJ (not U+0D00 / U+0D65).
    if char == "\u200d":
        return 2147483657
    if char == "\u200c":
        return 9
    o = ord(char)
    # Table has 112 entries: codepoints U+0D00 .. U+0D6F (see original BUILD_LIST 112).
    if o < 0x0D00 or o > 0x0D6F:
        return 0
    ch = o - 0x0D00
    return mlymCharClasses[ch]


def findSyllable(chars, prev, charCount):
    # Transitions use -1: return cursor *without* consuming current char (syllable end).
    # The port mistakenly used 5 everywhere row 1 had -1, so the FSM never stopped → one syllable per line → always guru pattern "−" → ശ്രീ.
    stateTable = [
        [1, 1, 1, 5, 3, 2, 1, 1, 1, 1, 1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 6, 1, -1, -1, -1, -1, 5, 4, -1, -1],
        [-1, 6, 1, -1, -1, -1, 2, 5, 4, 10, 9],
        [-1, -1, -1, -1, 3, 2, -1, -1, -1, 8, -1],
        [-1, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 7, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 3, 2, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 8, -1, 8],
    ]
    cursor = prev
    state = 0
    while cursor < charCount:
        charClass = getCharClass(chars[cursor])
        state = stateTable[state][charClass & 65535]
        if state < 0:
            return cursor
        cursor = cursor + 1
    return cursor
