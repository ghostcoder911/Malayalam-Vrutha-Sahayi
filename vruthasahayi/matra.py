# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1 matra.pyc

from .syllable import *
from .utils import *

def findCharType(sylChars):
    sylCharCount = len(sylChars)
    if sylCharCount == 1:
        if sylChars[0] in ('ആ', 'ഈ', 'ഊ', 'ഏ', 'ഐ', 'ഓ', 'ഔ'):
            return 'sg'
        else:
            return 'sl'
    elif sylCharCount == 2:
        if '്' in sylChars:
            for oneChar in sylChars:
                if oneChar in ('ണ', 'ന'):
                    return 'nch'
                if oneChar in ('ര', 'റ', 'ല', 'ള'):
                    return 'rlch'
                if oneChar >= 'ക' and oneChar <= 'ഹ':
                    return 'hc'

            return 'sl'
        for oneChar in sylChars:
            if oneChar in ('ാ', 'ീ', 'ൂ', 'േ', 'ൈ', 'ോ', 'ൌ', 'ൗ',
                           'ം', 'ഃ'):
                return 'sg'

        return 'sl'
    elif sylCharCount == 3:
        if 'ു' in sylChars:
            if '\u200d' in sylChars:
                return 'sl'
            elif '\u200c' in sylChars:
                for oneChar in sylChars:
                    if oneChar in ('െ', 'ആ'):
                        return 'nch'
                    if oneChar in ('ഈ', 'ഊ', 'ഏ', 'ഐ'):
                        return 'rlch'

            elif 'ഓ' in sylChars:
                for oneChar in sylChars:
                    if oneChar >= 'ഔ' and oneChar <= 'ണ':
                        return 'hc'

                return 'sl'
            else:
                return 'kl'
        for oneChar in sylChars:
            if oneChar == 'ന':
                for anotherChar in sylChars:
                    if anotherChar in ('ര', ):
                        return 'sl'
                    else:
                        return 'sg'

            elif oneChar == 'റ':
                return 'sg'

        return 'sg'
    elif sylChars[0] in ('ല', 'ള', 'ാ', 'ീ', 'ൂ', 'േ') and sylChars[1] == 'ൈ' and sylChars[2] == 'ോ':
        return 'ccc'
    if 'ൌ' in sylChars:
        if 'ൗ' in sylChars:
            return 'kl'
        elif 'ം' in sylChars:
            return 'kg'
    for oneChar in sylChars:
        if oneChar in ('ഃ', 'ണ', 'ന', 'ര', 'റ', 'ല', 'ള', 'ാ', 'ണ'):
            return 'kg'

    return 'kl'
    return


def getMatraArray(uniPadyam):
    strippedPadyam = changeNewLineToPipe(uniPadyam)
    charCount = len(strippedPadyam)
    prev = 0
    sylCount = 0
    lineSylCount = 0
    prevType = ' '
    glArray = []
    sylArray = []
    while prev < charCount:
        if not isMal(strippedPadyam[prev]):
            prev = prev + 1
            continue
        if strippedPadyam[prev] == '|':
            lineSylCount = 0
            glArray.append('|')
            sylArray.append((-1, -1))
            prevPrevType = prevType
            prevType = '|'
            prev = prev + 1
            sylCount = sylCount + 1
            continue
        syllable = findSyllable(strippedPadyam, prev, charCount)
        sylList = strippedPadyam[prev:syllable]
        charType = findCharType(sylList)
        if charType == 'sl':
            glArray.append('v')
            sylArray.append((prev, syllable - 1))
        elif charType == 'sg':
            glArray.append('-')
            sylArray.append((prev, syllable - 1))
        elif charType == 'kl':
            if sylCount > 0:
                if lineSylCount > 0:
                    glArray[sylCount - 1] = '-'
            glArray.append('v')
            sylArray.append((prev, syllable - 1))
        elif charType == 'kg':
            if sylCount > 0:
                if lineSylCount > 0:
                    glArray[sylCount - 1] = '-'
            glArray.append('-')
            sylArray.append((prev, syllable - 1))
        elif charType == 'nch':
            if sylCount > 0 and lineSylCount > 0:
                glArray[sylCount - 1] = '-'
                sylArray[sylCount - 1] = (sylArray[sylCount - 1][0], syllable - 1)
                sylCount = sylCount - 1
        elif charType == 'rlch':
            if sylCount > 0 and lineSylCount > 0:
                if glArray[sylCount - 1] != '-':
                    glArray[sylCount - 1] = 'c'
                sylArray[sylCount - 1] = (
                 sylArray[sylCount - 1][0], syllable - 1)
                sylCount = sylCount - 1
        elif charType == 'hc':
            if sylCount > 0 and lineSylCount > 0:
                glArray[sylCount - 1] = '-'
                sylArray[sylCount - 1] = (sylArray[sylCount - 1][0], syllable - 1)
                sylCount = sylCount - 1
        elif sylCount > 0 and lineSylCount > 0:
            if glArray[sylCount - 1] != '-':
                glArray[sylCount - 1] = 'c'
            sylArray[sylCount - 1] = (
             sylArray[sylCount - 1][0], sylArray[sylCount - 1][1] + 3)
            sylCount = sylCount - 1
            syllable = prev + 3
        prev = syllable
        prevPrevType = prevType
        prevType = charType
        lineSylCount = lineSylCount + 1
        sylCount = sylCount + 1

    return (
     glArray, sylArray)


