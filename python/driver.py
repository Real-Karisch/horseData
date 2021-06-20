import sys
import os
import re
import pandas as pd

if re.search('python$', os.getcwd()) is None:
    os.chdir('./python/')

from genInfoFns import parseGenInfo
from horseInfoFns import parseHorseInfo
from timesInfoFns import parseTimeInfo
from betInfoFns import parseBetInfo
from runlineInfoFns import parseRunlineInfo
from endInfoFns import parseEndInfo

from regexPatterns import *

def bulkParse(dirToFiles):
    if dirToFiles[-1] != '/':
        dirToFiles += '/'
    files = os.listdir(dirToFiles)

    fullDF = pd.DataFrame(columns=['trackName','month','day','year','raceNum','distance','surface','weather','conditions','startTime',
                                  'startNote','segment1','segment2','segment3','segment4','segment5','segments','lastRaceDay','lastRaceMonth',
                                  'lastRaceYear','lastRaceTrack','lastRaceNum','lastRacePlace','program','horse','jockey','weight','m_e',
                                  'placePP','placeSeg1','lengthsSeg1','placeSeg2','lengthsSeg2','placeSeg3','lengthsSeg3','placeSeg4',
                                  'lengthsSeg4','placeSeg5','lengthsSeg5','placeSeg6','lengthsSeg6','odds','comments','fracTime1','fracTime2',
                                  'fracTime3','fracTime4','fracTime5','finalTime','runUp','wpsPool','firstPlaceWin','firstPlacePlace',
                                  'firstPlaceShow','secondPlacePlace','secondPlaceShow','thirdPlaceShow','exactaBuyin','exactaFinish',
                                  'exactaPayout','exactaPool','trifectaBuyin','trifectaFinish','trifectaPayout','trifectaPool','superfectaBuyin',
                                  'superfectaFinish','superfectaPayout','superfectaPool','daily doubleBuyin','daily doubleFinish',
                                  'daily doublePayout','daily doublePool','rlPlaceSeg1','rlLengthsSeg1','rlPlaceSeg2','rlLengthsSeg2',
                                  'rlPlaceSeg3','rlLengthsSeg3','rlPlaceSeg4','rlLengthsSeg4','rlPlaceSeg5','rlLengthsSeg5','rlPlaceSeg6',
                                  'rlLengthsSeg6','trainer','owner'])
    
    cnt = 0
    for file in files:
        with open(dirToFiles + file) as active:
            chart = active.readlines()
        dayDF = parseFullDay(chart)

        fullDF = pd.concat([fullDF, dayDF])
        cnt += 1
    
    return fullDF

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

    #genRepeated = pd.concat([genItems] * horseItems.shape[0])
    #timesRepeated = pd.concat([timesItems] * horseItems.shape[0])
    #betRepeated = pd.concat([betItems] * horseItems.shape[0])

    #horseItems.reset_index(drop=True, inplace=True)
    #genRepeated.reset_index(drop=True, inplace=True)
    #timesRepeated.reset_index(drop=True, inplace=True)
    #betRepeated.reset_index(drop=True, inplace=True)
    #runlineItems.reset_index(drop=True, inplace=True)  
    """
    outDF = pd.concat([genRepeated, horseItems, timesRepeated, betRepeated], axis = 1)
    outDF = pd.merge(outDF, runlineItems, how='outer', on='program')
    outDF = pd.merge(outDF, endItems, how='outer', on='program')
    """

    outputDict = {
        'general': genItems,
        'horse': horseItems,
        'times': timesItems,
        'bet': betItems,
        'runline': runlineItems,
        'end': endItems
    }

    return outputDict