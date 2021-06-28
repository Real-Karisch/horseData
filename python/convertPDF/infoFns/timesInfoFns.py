import re
import pandas as pd

from .regexPatterns import *

def parseTimeInfo(timeLines):
    timeDict = {}

    runUp = '0'

    for line in timeLines:
        if re.search(fractionalTimesLinePattern, line) is not None:
            fractionalTimes = parseFractionalTimes(line)
        elif re.search(runupLinePattern, line) is not None:
            runUp = parseRunUp(line)

    timeDict['fracTime1'] = fractionalTimes[0]
    timeDict['fracTime2'] = fractionalTimes[1]
    timeDict['fracTime3'] = fractionalTimes[2]
    timeDict['fracTime4'] = fractionalTimes[3]
    timeDict['fracTime5'] = fractionalTimes[4]
    timeDict['finalTime'] = fractionalTimes[5]
    timeDict['runUp'] = runUp

    return timeDict


def parseFractionalTimes(line):

    fullSearch = re.search(fractionalTimesSearchPattern, line)

    if fullSearch is None:
        print('Match error in parseFractionalTimes on line: ' + line)
        return ['ERROR'] * 7

    out = []
    for i in range(2,8):
        if fullSearch.group(i) is None or fullSearch.group(i) == 'N/A':
            out.append('')
        else:
            out.append(fullSearch.group(i))

    return out

def parseRunUp(line):
    fullSearch = re.search(runupSearchPattern, line)
    runUp = fullSearch.group(1)

    return runUp