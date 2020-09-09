import re
import pandas as pd

def parseRunlineInfo(runlineLines):
    lines = runlineLines[2:]

    numHorses = int(len(lines) / 2)

    #set up empty dataframe
    runlineDF = pd.DataFrame()

    for i in [x*2 for x in list(range(numHorses))]:
        runlineDict = {}

        activeHorse = lines[i:i+2]

        topItems = parseRunlineTopLine(activeHorse[0])
        bottomItems = parseRunlineBottomLine(activeHorse[1])

        #if all 6 segments have lengths
        if [x for x in topItems if x == ''] == []:
            runlineDict['rlLengthsSeg1'] = topItems[0] #fill in the first segment with the first length
            startInd = 1 #filling in the remaining lengths will follow with the next element
        else:
            runlineDict['rlLengthsSeg1'] = '' #otherwise it will be "Start" and won't have any lengths associated
            startInd = 0 #fill in remaining elements starting from the beginning of the list

        runlineDict['rlLengthsSeg2'] = topItems[startInd]
        runlineDict['rlLengthsSeg3'] = topItems[startInd + 1]
        runlineDict['rlLengthsSeg4'] = topItems[startInd + 2]
        runlineDict['rlLengthsSeg5'] = topItems[startInd + 3]
        runlineDict['rlLengthsSeg6'] = topItems[startInd + 4]

        runlineDict['program'] = bottomItems[0]
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