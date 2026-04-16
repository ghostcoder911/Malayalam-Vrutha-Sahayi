# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1
import re

from . import data

def findVrutham(glArray):
    glString = ('').join(glArray)
    glString += '|'
    glLines = glString.split('|')
    glLines = glLines[:len(glLines) - 1]
    vruthamList = []
    lineCount = 1
    slokamCount = 1
    printSummary = 0
    slokaLakshanamList = []
    slokamLinesList = []
    anushtupSlokam = []
    for i in glLines:
        yathiPos = ()
        if i == '':
            if printSummary == 1:
                (lineVruthamIds, slokaVruthamId) = findSlokaVrutham(slokaLakshanamList, slokamLinesList)
                for num in range(1, len(lineVruthamIds) + 1):
                    if num == 1:
                        if slokaVruthamId != -1:
                            sV = slokaVruthamId
                        else:
                            sV = -1
                    else:
                        sV = -2
                    if data.vruthamTable[lineVruthamIds[len(lineVruthamIds) - num]][2] > 277:
                        yathiPositions = (-1, -1)
                    else:
                        yathiPositions = vruthamList[len(vruthamList) - num][4]
                    vruthamList[len(vruthamList) - num] = (
                     vruthamList[len(vruthamList) - num][0], vruthamList[len(vruthamList) - num][1], lineVruthamIds[len(lineVruthamIds) - num], sV, yathiPositions)

                slokamCount += 1
                printSummary = 0
            slokaLakshanamList = []
            slokamLinesList = []
            anushtupSlokam = []
            lineCount = 1
            continue
        printSummary = 1
        if len(i) == 8:
            anushtupSlokam.append(i)
        if i in data.vruthamDict:
            vruthamId = data.vruthamDict[i]
            if vruthamId in data.yathiDict:
                yathiPos = data.yathiDict[vruthamId]
            vruthamList.append((str(slokamCount), str(lineCount), vruthamId, -2, yathiPos))
        elif 'c' in i:
            vruthamId = convolutedFindVrutham(i, data.vruthamDict)
            if vruthamId >= 0:
                if vruthamId in data.yathiDict:
                    yathiPos = data.yathiDict[vruthamId]
                vruthamList.append((str(slokamCount), str(lineCount), vruthamId, -2, yathiPos))
            else:
                vruthamList.append((str(slokamCount), str(lineCount), -1, -2, (-1, -1)))
        else:
            vruthamId = -1
            vruthamList.append((str(slokamCount), str(lineCount), -1, -2, (-1, -1)))
        slokaLakshanamList.append(vruthamId)
        slokamLinesList.append(i)
        if lineCount == 4:
            (lineVruthamIds, slokaVruthamId) = findSlokaVrutham(slokaLakshanamList, slokamLinesList)
            if slokaVruthamId == -1 and len(anushtupSlokam) == 4:
                (lineVruthamIds, slokaVruthamId) = checkIfAnushtupFamily(anushtupSlokam)
            for num in range(1, len(lineVruthamIds) + 1):
                if num == 1:
                    if slokaVruthamId != -1:
                        sV = slokaVruthamId
                    else:
                        sV = -1
                else:
                    sV = -2
                if data.vruthamTable[lineVruthamIds[4 - num]][2] > 277:
                    yathiPositions = (-1, -1)
                else:
                    yathiPositions = vruthamList[len(vruthamList) - num][4]
                vruthamList[len(vruthamList) - num] = (
                 vruthamList[len(vruthamList) - num][0], vruthamList[len(vruthamList) - num][1], lineVruthamIds[4 - num], sV, yathiPositions)

            printSummary = 0
            lineCount = 0
            slokamCount += 1
            slokaLakshanamList = []
            slokamLinesList = []
            anushtupSlokam = []
        lineCount += 1

    return vruthamList


def convolutedFindVrutham(i, dict):
    if 'c' in i:
        il = i.replace('c', 'v', 1)
        id = convolutedFindVrutham(il, dict)
        if id >= 0:
            return id
        ig = i.replace('c', '-', 1)
        id = convolutedFindVrutham(ig, dict)
        return id
    else:
        if i in dict:
            id = dict[i]
        else:
            id = -1
        return id
    return


def findSlokaVrutham(slokaLakshanamList, slokamLinesList):
    prevVruthamId = -2
    for i in slokaLakshanamList:
        if prevVruthamId != -2 and i != prevVruthamId:
            break
        else:
            vruthamId = i
        if i == -1:
            break
        prevVruthamId = i
    else:
        return (
         slokaLakshanamList, vruthamId)

    return findArdhaVishamaVrutham(slokamLinesList, slokaLakshanamList)


def findArdhaVishamaVrutham(slokamLinesList, slokaLakshanamList):
    newLineVruthamIdsString = ''
    newLineVruthamIds = []
    for oneLine in slokamLinesList:
        newLineVruthamIds.append(convolutedFindVrutham(oneLine, data.avGanamDict))

    for i in newLineVruthamIds:
        newLineVruthamIdsString += str(i)
        newLineVruthamIdsString += '-'

    if newLineVruthamIdsString in data.ardhaVishamaVruthamDict:
        slokaVruthamId = data.ardhaVishamaVruthamDict[newLineVruthamIdsString]
        return (newLineVruthamIds, slokaVruthamId)
    else:
        return (
         slokaLakshanamList, -1)
    return


def checkIfAnushtupFamily(anushtupSlokam):
    slokaVruthamId = -1
    lineVruthamIds = []
    for j in range(0, 4):
        lineVruthamIds.append(-1)

    anushtupSlokamString = ''
    for line in anushtupSlokam:
        anushtupSlokamString += line
        anushtupSlokamString += '|'

    vakthram = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[vc][\\-c][\\-c])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>[vc][\\-c][\\-c])(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[vc][\\-c][\\-c])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>[vc][\\-c][\\-c])(?P<l4char2>.)(?P<sep4>[|])')
    if vakthram.match(anushtupSlokamString):
        slokaVruthamId = 286
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    pathyaVakthram = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[vc][\\-c][\\-c])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>[vc][\\-c][vc])(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[vc][\\-c][\\-c])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>[vc][\\-c][vc])(?P<l4char2>.)(?P<sep4>[|])')
    if pathyaVakthram.match(anushtupSlokamString):
        slokaVruthamId = 171
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    vipareethaPathyaVakthram = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[vc][\\-c][vc])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>[vc][\\-c][\\-c])(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[vc][\\-c][vc])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>[vc][\\-c][\\-c])(?P<l4char2>.)(?P<sep4>[|])')
    if vipareethaPathyaVakthram.match(anushtupSlokamString):
        slokaVruthamId = 302
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    chapalaVakthram = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[vc][vc][vc])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>[vc][\\-c][\\-c])(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[vc][vc][vc])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>[vc][\\-c][\\-c])(?P<l4char2>.)(?P<sep4>[|])')
    if chapalaVakthram.match(anushtupSlokamString):
        slokaVruthamId = 118
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    bhaVipula = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[\\-c][vc][vc])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>(([\\-c][vc][vc])|([vc][\\-c][\\-c])))(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[\\-c][vc][vc])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>(([\\-c][vc][vc])|([vc][\\-c][\\-c])))(?P<l4char2>.)(?P<sep4>[|])')
    if bhaVipula.match(anushtupSlokamString):
        slokaVruthamId = 207
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    naVipula = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[vc][vc][vc])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>(([vc][vc][vc])|([vc][\\-c][\\-c])))(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[vc][vc][vc])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>(([vc][vc][vc])|([vc][\\-c][\\-c])))(?P<l4char2>.)(?P<sep4>[|])')
    if naVipula.match(anushtupSlokamString):
        slokaVruthamId = 161
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    raVipula = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[\\-c][vc][\\-c])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>(([\\-c][vc][\\-c])|([vc][\\-c][\\-c])))(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[\\-c][vc][\\-c])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>(([\\-c][vc][\\-c])|([vc][\\-c][\\-c])))(?P<l4char2>.)(?P<sep4>[|])')
    if raVipula.match(anushtupSlokamString):
        slokaVruthamId = 269
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    maVipula = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[\\-c][\\-c][\\-c])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>(([\\-c][\\-c][\\-c])|([vc][\\-c][\\-c])))(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[\\-c][\\-c][\\-c])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>(([\\-c][\\-c][\\-c])|([vc][\\-c][\\-c])))(?P<l4char2>.)(?P<sep4>[|])')
    if maVipula.match(anushtupSlokamString):
        slokaVruthamId = 245
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    thaVipula = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>[\\-c][\\-c][vc])(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>(([\\-c][\\-c][vc])|([vc][\\-c][\\-c])))(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>[\\-c][\\-c][vc])(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>(([\\-c][\\-c][vc])|([vc][\\-c][\\-c])))(?P<l4char2>.)(?P<sep4>[|])')
    if thaVipula.match(anushtupSlokamString):
        slokaVruthamId = 139
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    anushtup = re.compile('(?P<l1char1>.)(?P<l1gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l1gan2>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][vc][vc])|([\\-c][\\-c][\\-c])))(?P<l1char2>.)(?P<sep1>[|])(?P<l2char1>.)(?P<l2gan1>(([vc][\\-c][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l2gan2>[vc][\\-c][vc])(?P<l2char2>.)(?P<sep2>[|])(?P<l3char1>.)(?P<l3gan1>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l3gan2>(([vc][\\-c][\\-c])|([\\-c][vc][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][vc][vc])|([\\-c][\\-c][\\-c])))(?P<l3char2>.)(?P<sep3>[|])(?P<l4char1>.)(?P<l4gan1>(([vc][\\-c][\\-c])|([\\-c][\\-c][vc])|([\\-c][vc][vc])|([vc][\\-c][vc])|([\\-c][\\-c][\\-c])))(?P<l4gan2>[vc][\\-c][vc])(?P<l4char2>.)(?P<sep4>[|])')
    if anushtup.match(anushtupSlokamString):
        slokaVruthamId = 10
        lineVruthamIds = []
        for j in range(0, 4):
            lineVruthamIds.append(slokaVruthamId)

        return (
         lineVruthamIds, slokaVruthamId)
    return (lineVruthamIds, slokaVruthamId)


