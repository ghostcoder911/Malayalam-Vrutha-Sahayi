# -*- coding: utf-8 -*-
# Ported from Vrutha Sahayi 0.1 interface.pyc
from . import data
from .checkvrutham import *
from .findvrutham import *
from .matra import *
from .utils import *


def markCorrectSyls(errlocs, sylArray):
    modArray = []
    for i in range(0, len(errlocs)):
        if errlocs[i] == "x":
            modArray.append((sylArray[i], "n"))
        elif errlocs[i] == "t":
            modArray.append((sylArray[i], "t"))
        elif errlocs[i] == "g":
            modArray.append((sylArray[i], "g"))
        else:
            modArray.append((sylArray[i], "y"))

    return modArray


def getVrutham(padyam, vrutham):
    errlocs = []
    modArray = []
    if padyam == "":
        return ("No Padyam Given", errlocs)
    (glArray, sylArray) = getMatraArray(padyam)
    if vrutham != "":
        errlocs = checkVrutham(vrutham, glArray)
        modArray = markCorrectSyls(errlocs, sylArray)
        return (errlocs, modArray)
    else:
        vrutham = findVrutham(glArray)
        prevPos = -1
        newLinePos = 0
        multipleVruthams = 0
        prevSlokamNumber = -2
        prevLineVruthamId = -2
        for i in range(0, len(vrutham)):
            curPos = sylArray.index((-1, -1), newLinePos)
            while curPos - prevPos < 2:
                prevPos = curPos
                newLinePos += 1
                curPos = sylArray.index((-1, -1), newLinePos)

            sylLine = sylArray[prevPos + 1 : curPos]
            yathiBool = "y"
            if vrutham[i][2] != -1:
                if vrutham[i][2] in data.similarVruthamDict:
                    similarVruthamList = data.similarVruthamDict[vrutham[i][2]]
                    for vruthamId in similarVruthamList:
                        if vruthamId in data.yathiDict:
                            yathiPos = data.yathiDict[vruthamId]
                            yathiBool = "y"
                            for j in yathiPos:
                                if j == -1:
                                    continue
                                if (
                                    " "
                                    not in padyam[sylLine[j - 1][1] : sylLine[j][0]]
                                    and "/"
                                    not in padyam[sylLine[j - 1][1] : sylLine[j][0]]
                                ):
                                    yathiBool = "n"
                                    break

                            if yathiBool == "y":
                                lineVruthamId = vruthamId
                                break
                            else:
                                lineVruthamId = vrutham[i][2]
                        else:
                            yathiBool = "y"
                            continue

                    newSlokaVruthamId = lineVruthamId
                    if prevSlokamNumber != -2 and vrutham[i][0] != prevSlokamNumber:
                        multipleVruthams = 0
                    elif prevLineVruthamId != -2 and lineVruthamId != prevLineVruthamId:
                        multipleVruthams = 1
                    if vrutham[i][3] != -2 and vrutham[i][3] != -1:
                        if multipleVruthams == 1:
                            slokaVruthamId = -1
                        else:
                            slokaVruthamId = newSlokaVruthamId
                    else:
                        slokaVruthamId = vrutham[i][3]
                    prevSlokamNumber = vrutham[i][0]
                    prevLineVruthamId = lineVruthamId
                else:
                    lineVruthamId = vrutham[i][2]
                    slokaVruthamId = vrutham[i][3]
                    for j in vrutham[i][4]:
                        if j == -1:
                            continue
                        if (
                            " " not in padyam[sylLine[j - 1][1] : sylLine[j][0]]
                            and "/" not in padyam[sylLine[j - 1][1] : sylLine[j][0]]
                        ):
                            yathiBool = "n"
                            break

            else:
                lineVruthamId = vrutham[i][2]
                slokaVruthamId = vrutham[i][3]
            vrutham[i] = (
                vrutham[i][0],
                vrutham[i][1],
                lineVruthamId,
                slokaVruthamId,
                yathiBool,
            )
            prevPos = curPos
            newLinePos += 1

    return (vrutham, modArray)
