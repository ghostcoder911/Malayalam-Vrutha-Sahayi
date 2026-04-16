# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1 utils.pyc


def changeNewLineToPipe(strString):
    strippedString = strString.replace("\n", "|")
    if strippedString[len(strippedString) - 1] != "|":
        strippedString += "|"
    return strippedString
