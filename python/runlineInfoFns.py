import re
import pandas as pd

def parseRunlineInfo(runlineLines):
    lines = runlineLines[2:]

    numHorses = int(len(lines) / 2)

    runlineDF = pd.DataFrame(columns=['rlPgm', 'rlPlaceSeg1','rlLengthsSeg1','rlPlaceSeg2','rlLengthsSeg2','rlPlaceSeg3',
                                    'rlLengthsSeg3','rlPlaceSeg4','rlLengthsSeg4','rlPlaceSeg5','rlLengthsSeg5','rlPlaceFin',
                                    'rlLengthsFin'])

    for i in [x*2 for x in list(range(numHorses))]:
        runlineDict = {}

        activeHorse = lines[i:i+2]

        topItems = parseRunlineTopLine(activeHorse[0])
        bottomItems = parseRunlineBottomLine(activeHorse[1])

        runlineDict['rlLengthsSeg1'] = topItems[0]
        runlineDict['rlLengthsSeg2'] = topItems[1]
        runlineDict['rlLengthsSeg3'] = topItems[2]
        runlineDict['rlLengthsSeg4'] = topItems[3]
        runlineDict['rlLengthsSeg5'] = topItems[4]
        runlineDict['rlLengthsSeg6'] = topItems[5]

        runlineDict['rlPgm'] = bottomItems[0]
        runlineDict['rlPlaceSeg1'] = bottomItems[1]
        runlineDict['rlPlaceSeg2'] = bottomItems[2]
        runlineDict['rlPlaceSeg3'] = bottomItems[3]
        runlineDict['rlPlaceSeg4'] = bottomItems[4]
        runlineDict['rlPlaceSeg5'] = bottomItems[5]
        runlineDict['rlPlaceSeg6'] = bottomItems[6]

        activeDF = pd.DataFrame(runlineDict, index = [0])

        runlineDF = pd.concat([runlineDF, activeDF])

    return runlineDF


def parseRunlineTopLine(line):
    fullSearch = re.search(r'([0-9/A-Za-z]+) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*)$', line)

    out = []
    for i in range(1,7):
        out.append(fullSearch.group(i))

    return out

def parseRunlineBottomLine(line):
    fullSearch = re.search(r'^ (\d?\d) [^0-9]+ ([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*)$', line)

    out = []

    for i in range(1,8):
        out.append(fullSearch.group(i))

    return out