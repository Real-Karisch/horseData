import re
import pandas as pd

from regexPatterns import *

def parseEndInfo(endLines):

    cnt = 0
    for line in endLines:
        if re.match(trainerLinePattern, line) is not None:
            trainerInd = [cnt]
        elif re.match(ownerLinePattern, line) is not None:
            trainerInd.append(cnt)
            ownerInd = [cnt]
        elif re.match(footnoteLinePattern, line) is not None:
            ownerInd.append(cnt)
        cnt += 1
    
    trainerLine = ''.join([line[:-1] for line in endLines[trainerInd[0]: trainerInd[1]]]) + ';'
    ownerLine = ''.join([line[:-1] for line in endLines[ownerInd[0]: ownerInd[1]]])

    trainersDict = parseTrainerLine(trainerLine)
    ownersDict = parseOwnerLine(ownerLine)

    return [trainersDict, ownersDict]


def parseTrainerLine(line):
    endDict = {'program': [], 'trainer': []}

    fullSearch = re.search(trainerFullSearchPattern, line)
    split = fullSearch.group(0).split(';')[:-1]

    for item in split:
        shortSearch = re.search(trainerShortSearchPattern, item)

        endDict['program'].append(shortSearch.group(1))
        endDict['trainer'].append(shortSearch.group(2))

    return endDict

def parseOwnerLine(line):
    endDict = {'program': [], 'owner': []}

    fullSearch = re.search(ownerFullSearchPattern, line)
    split = fullSearch.group(0).split(';')[:-1]

    for item in split:
        shortSearch = re.search(ownerShortSearchPattern, item)

        endDict['program'].append(shortSearch.group(1))
        endDict['owner'].append(shortSearch.group(2))

    return endDict