# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1
import re

from . import data

def getGlSeq(vruthamId):
    return data.vruthamTable[vruthamId][4]


def checkVrutham(uniVrutham, glArray):
    glString = ('').join(glArray)
    glLines = glString.split('|')
    glLines = glLines[:len(glLines) - 1]
    vruthamId = data.getVruthamId(uniVrutham)
    ardhaVishamaVrutham = 'n'
    upajathiVrutham = 'n'
    if vruthamId == -1:
        return [
         ((-1, -1), 'n')]
    glSeq = getGlSeq(vruthamId)
    if vruthamId in data.yathiDict:
        yathiPos = data.yathiDict[vruthamId]
    else:
        yathiPos = (-1, -1)
    if glSeq == 'ANUSHTUP':
        errLocs = checkVruthamForAnushtupFamily(vruthamId, glLines)
        return errLocs
    elif glSeq[0:2] == 'AV':
        ardhaVishamaVrutham = 'y'
        glSeq = glSeq[3:len(glSeq)]
        glSeqLines = glSeq.split('|')
        if vruthamId in (49, 50):
            upajathiVrutham = 'y'
    posCount = 0
    errLocs = []
    lineNum = 0
    for oneLine in glLines:
        if oneLine == '':
            errLocs.append('|')
            lineNum = 0
            continue
        if ardhaVishamaVrutham == 'y':
            glSeqLine = glSeqLines[lineNum % 4]
        else:
            glSeqLine = glSeq
        lineNum = lineNum + 1
        posCount = 0
        for i in oneLine:
            if posCount > len(glSeqLine) - 1:
                errLocs.append('x')
            elif upajathiVrutham == 'y' and posCount == 0:
                errLocs.append(i)
            elif posCount == len(glSeqLine) - 1 and vruthamId not in (100, 337):
                errLocs.append(i)
            elif i == glSeqLine[posCount] or i == 'c':
                if posCount + 1 in yathiPos[1:]:
                    errLocs.append('t')
                else:
                    errLocs.append(i)
            else:
                errLocs.append('x')
            posCount = posCount + 1

        errLocs.append('|')

    return errLocs


def checkVruthamForAnushtupFamily(vruthamId, glLines):
    errLocs = []
    lineNum = 0
    for oneLine in glLines:
        if oneLine == '':
            errLocs.append('|')
            lineNum = 0
            continue
        lineNum = lineNum + 1
        curErrLocs = []
        curErrLocs.append('a')
        if vruthamId == 10:
            if lineNum % 2 == 1:
                ganam1 = re.compile('^.(?=(([vc][vc][vc])|([vc][vc][\\-c])))')
            else:
                ganam1 = re.compile('^.(?=(([\\-c][vc][\\-c])|([vc][vc][vc])|([vc][vc][\\-c])))')
        else:
            ganam1 = re.compile('^.(?=(([vc][vc][vc])|([vc][vc][\\-c])))')
        if ganam1.search(oneLine):
            curErrLocs.extend(['g', 'g', 'g'])
        else:
            curErrLocs.extend(['a', 'a', 'a'])
        if vruthamId == 286:
            ganam2 = re.compile('^....(?![vc][\\-c][\\-c])')
        elif vruthamId == 171:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![vc][\\-c][\\-c])')
            else:
                ganam2 = re.compile('^....(?![vc][\\-c][vc])')
        elif vruthamId == 302:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![vc][\\-c][vc])')
            else:
                ganam2 = re.compile('^....(?![vc][\\-c][\\-c])')
        elif vruthamId == 118:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![vc][vc][vc])')
            else:
                ganam2 = re.compile('^....(?![vc][\\-c][\\-c])')
        elif vruthamId == 207:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![\\-c][vc][vc])')
            else:
                ganam2 = re.compile('^....(?!(([\\-c][vc][vc])|([vc][\\-c][\\-c])))')
        elif vruthamId == 161:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![vc][vc][vc])')
            else:
                ganam2 = re.compile('^....(?!(([vc][vc][vc])|([vc][\\-c][\\-c])))')
        elif vruthamId == 269:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![\\-c][vc][\\-c])')
            else:
                ganam2 = re.compile('^....(?!(([\\-c][vc][\\-c])|([vc][\\-c][\\-c])))')
        elif vruthamId == 245:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![\\-c][\\-c][\\-c])')
            else:
                ganam2 = re.compile('^....(?!(([\\-c][\\-c][\\-c])|([vc][\\-c][\\-c])))')
        elif vruthamId == 139:
            if lineNum % 2 == 1:
                ganam2 = re.compile('^....(?![\\-c][\\-c][vc])')
            else:
                ganam2 = re.compile('^....(?!(([\\-c][\\-c][vc])|([vc][\\-c][\\-c])))')
        elif lineNum % 2 == 1:
            ganam2 = re.compile('^.(?=(([vc][\\-c][vc])|([vc][vc][\\-c])))')
        else:
            ganam2 = re.compile('^....(?![vc][\\-c][vc])')
        if ganam2.search(oneLine):
            curErrLocs.extend(['g', 'g', 'g'])
        else:
            curErrLocs.extend(['a', 'a', 'a'])
        curErrLocs.append('a')
        if len(oneLine) > 8:
            for i in range(0, len(oneLine) - 8):
                curErrLocs.append('x')

        curErrLocs = curErrLocs[0:len(oneLine)]
        errLocs.extend(curErrLocs)
        errLocs.append('|')

    return errLocs


