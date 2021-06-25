import re
import pandas as pd

from .regexPatterns import *

def parseRunlineInfo(runlineLines):
    runlineLines = [x for x in runlineLines if re.search('^ \([A-Z]+\)$', x) is None]

    colsSearch = re.search(pointOfCallLinePattern, runlineLines[1])
    if colsSearch.group(1) == 'Start':
        firstCallStart = True
    else:
        firstCallStart = False
    
    lines = runlineLines[2:]

    numHorses = int(len(lines) / 2)

    #set up empty dataframe
    runlineDicts = []

    priorLineBottom = True
    missingTopLineInd = []
    for i in range(len(runlineLines)): #loop to add spacing if top line missing (can only happen if horse dropped out of race before first point of call)
        line = runlineLines[i]
        if firstCallStart:
            checkSearch = re.search(firstCallStartRLSearchPattern, line)
        else:
            checkSearch = re.search(firstCallNonStartRLSearchPattern, line)

        if checkSearch is not None and priorLineBottom: #check to see if the current line meets the conditions for a missing top line and whether the last line was bottom
            missingTopLineInd.append(i) #add index where true
            priorLineBottom = True
        else:
            priorLineBottom = False

    for i in range(len(missingTopLineInd)): #now need to loop over indices and insert empty spacer lines
        runlineLines.insert(missingTopLineInd[i], ' ')
        missingTopLineInd = [x + 1 for x in missingTopLineInd] #need to increment remaining indices to account for new element

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

        runlineDicts.append(dict(runlineDict))

    return runlineDicts


def parseRunlineTopLine(line):
    fullSearch = re.search(rlTopLineSearchPattern, line)

    if fullSearch is None:
        print('Match error in parseRunlineTopLine on line: ' + line)
        return ['ERROR'] * 6

    out = []
    for i in range(1,7):
        out.append(fullSearch.group(i))

    return out

def parseRunlineBottomLine(line):
    fullSearch = re.search(rlBottomLineSearchPattern, line)
    if fullSearch is None:
        print('Match error in parseRunlineBottomLine on line: ' + line)
        return ['ERROR'] * 7

    out = []

    for i in range(1,8):
        out.append(fullSearch.group(i))

    return out