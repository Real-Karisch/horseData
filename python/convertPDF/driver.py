import sys
import os
import re
import pandas as pd

if __name__ == '__main__':
    from infoFns.genInfoFns import parseGenInfo
    from infoFns.horseInfoFns import parseHorseInfo
    from infoFns.timesInfoFns import parseTimeInfo
    from infoFns.betInfoFns import parseBetInfo
    from infoFns.runlineInfoFns import parseRunlineInfo
    from infoFns.endInfoFns import parseEndInfo

    from infoFns.regexPatterns import *

else:
    from .infoFns.genInfoFns import parseGenInfo
    from .infoFns.horseInfoFns import parseHorseInfo
    from .infoFns.timesInfoFns import parseTimeInfo
    from .infoFns.betInfoFns import parseBetInfo
    from .infoFns.runlineInfoFns import parseRunlineInfo
    from .infoFns.endInfoFns import parseEndInfo

    from .infoFns.regexPatterns import *

def parseFullDay(fullChart):
    newRaceInd = [-1] #first index will be 0 after conversion (controls for out of index error later)
    for i in range(len(fullChart)):
        if re.search(newRaceTest, fullChart[i]) is not None: #check for the expression that signifies end of race
            newRaceInd.append(i)

    allRaces = []
    for i in range(len(newRaceInd) - 1):
        #print('Race number: ' + str(i))
        allRaces.append(parseRace(fullChart[newRaceInd[i] + 1:newRaceInd[i + 1]]))

    return allRaces

def parseRace(raceChart):
    cnt = 0

    #loop to find indexes for different parse sections
    for line in raceChart:
        if re.search(cancelledRace, line) is not None: #check for cancelled race first, if cancelled, return empty dictionary
            return {}
        elif re.search(quarterHorseRace, line) is not None: #also do not need to process quarter horses
            return {}
        elif re.search(generalInfoCutoff, line) is not None: #everything before this falls under "general info"
            genInd = cnt + 1
            horseInd = [cnt + 1]
        elif re.search(horseInfoCutoff, line) is not None: #after general info, need to process info for each horse
            horseInd.append(cnt)
            timesInd = [cnt]
        elif re.search(timesInfoCutoff, line) is not None: #after horses, timing and runup info
            timesInd.append(cnt + 1)
            betInd = [cnt + 1]
        elif re.search(betInfoCutoff, line) is not None: #after timing, betting info and additional horse info
            betInd.append(cnt)
            runLineInd = [cnt]
        elif re.search(endInfoCutoff, line) is not None: #finally, need to do trainers, owners and other ending info
            runLineInd.append(cnt)
            endInfoInd = cnt
        cnt += 1
    
    genItems = parseGenInfo(raceChart[:genInd])
    horseItems = parseHorseInfo(raceChart[horseInd[0]:horseInd[1]])
    timesItems = parseTimeInfo(raceChart[timesInd[0]:timesInd[1]])
    betItems = parseBetInfo(raceChart[betInd[0]:betInd[1]])
    runlineItems = parseRunlineInfo(raceChart[runLineInd[0]:runLineInd[1]])
    endItems = parseEndInfo(raceChart[endInfoInd:])

    outputDict = {
        'general': genItems,
        'horse': horseItems,
        'times': timesItems,
        'bet': betItems,
        'runline': runlineItems,
        'end': endItems
    }

    return outputDict



######### DEBUG
if __name__ == '__main__':
    with open('./../charts/txts/eqbPDFChartPlus - 2021-06-25T163456.691.txt') as file:
        full = file.readlines()
        jack = parseFullDay(full)