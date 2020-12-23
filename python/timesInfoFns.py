import re
import pandas as pd

def parseTimeInfo(timeLines):

    timeDF = pd.DataFrame()
    timeDict = {}

    runUp = '0'

    for line in timeLines:
        if re.search('Fractional Times:|Final Time:', line) is not None:
            fractionalTimes = parseFractionalTimes(line)
        elif re.search('Run-Up:', line) is not None:
            runUp = parseRunUp(line)

    timeDict['fracTime1'] = fractionalTimes[0]
    timeDict['fracTime2'] = fractionalTimes[1]
    timeDict['fracTime3'] = fractionalTimes[2]
    timeDict['fracTime4'] = fractionalTimes[3]
    timeDict['fracTime5'] = fractionalTimes[4]
    timeDict['finalTime'] = fractionalTimes[5]
    timeDict['runUp'] = runUp

    return pd.DataFrame(timeDict, index=[0])


def parseFractionalTimes(line):

    fullSearch = re.search(r'(Fractional Times: ([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*))? Final Time: ([0-9.:]*)', line)

    out = []
    for i in range(2,8):
        if fullSearch.group(i) is None:
            out.append('')
        else:
            out.append(fullSearch.group(i))

    return out

def parseRunUp(line):
    fullSearch = re.search(r'Run-Up: ([0-9.]*)', line)
    runUp = fullSearch.group(1)

    return runUp