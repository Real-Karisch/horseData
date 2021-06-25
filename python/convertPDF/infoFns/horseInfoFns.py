import re
import pandas as pd

from .regexPatterns import *

def parseHorseInfo(horseLines):
    numHorses = int(len(horseLines) / 2)

    horseDict = {}
    horseDicts = []

    priorLineBottom = True
    missingTopLineInd = []
    for i in range(len(horseLines)): #loop to add spacing if top line missing (can only happen if horse has never been raced AND was in last place the whole race)
        line = horseLines[i]
        if re.search(horseInfoBottomLineCheckPattern, line) is not None: #check to see if the current line is bottom and the last line was also bottom
            if priorLineBottom:
                missingTopLineInd.append(i) #add index where true
            priorLineBottom = True
        else:
            priorLineBottom = False

    for i in range(len(missingTopLineInd)): #now need to loop over indices and insert empty spacer lines
        horseLines.insert(missingTopLineInd[i], ' ')
        missingTopLineInd = [x + 1 for x in missingTopLineInd] #need to increment remaining indices to account for new element

    topItemsList = []
    #loop over each horse in the lines provided
    for i in [x*2 for x in list(range(numHorses))]:
        activeHorse = horseLines[i:i+2]
        bottomItems = parseHorseBottomLine(activeHorse[1])
        topItems = parseHorseTopLine(activeHorse[0])

        horseDict['lastRaceDay'] = bottomItems[0]
        horseDict['lastRaceMonth'] = bottomItems[1]
        horseDict['lastRaceYear'] = bottomItems[2]
        horseDict['lastRaceTrack'] = bottomItems[3]
        horseDict['program'] = bottomItems[4]
        horseDict['horse'] = bottomItems[5].strip()
        horseDict['jockey'] = bottomItems[6]
        horseDict['weight'] = bottomItems[7]
        horseDict['m_e'] = bottomItems[8]
        horseDict['placePP'] = bottomItems[9]
        horseDict['placeSeg1'] = bottomItems[10]
        horseDict['placeSeg2'] = bottomItems[11]
        horseDict['placeSeg3'] = bottomItems[12]
        horseDict['placeSeg4'] = bottomItems[13]
        horseDict['placeSeg5'] = bottomItems[14]
        horseDict['placeSeg6'] = bottomItems[15]
        horseDict['odds'] = bottomItems[16]
        horseDict['comments'] = bottomItems[17]

        if horseDict['lastRaceDay'] == '':
            horseDict['lastRaceNum'] = ''
            horseDict['lastRacePlace'] = ''
            topItemsList.append(topItems)

            horseDicts.append(dict(horseDict))
        else:
            horseDict['lastRaceNum'] = topItems[0]
            horseDict['lastRacePlace'] = topItems[1]
            topItemsList.append(topItems[2:])

            horseDicts.append(dict(horseDict))
    
    horseDicts = placeLengths(horseDicts, topItemsList)

    return horseDicts

def parseHorseTopLine(line):
    fullSearch = re.search(horseInfoTopLineSearchPattern, line)

    out = []
    for i in range(1,9):
        out.append(fullSearch.group(i))

    return out

def parseHorseBottomLine(line):
    
    fullSearch = re.search(horseInfoBottomLineSearchPattern, line)
    if fullSearch is None:
        print('parseHorseBottomLine error on line: ' + line)
        out = ['ERROR'] * 18
        return out
    out = []
    dateSearch = re.search(horseInfoDateSearchPattern, fullSearch.group(1))
    if dateSearch is not None:
        out[:4] = [dateSearch.group(1), dateSearch.group(2), dateSearch.group(3), dateSearch.group(4)]
    else:
        out[:4] = [''] * 4
    
    out.append(fullSearch.group(2))

    horseAndJockey = fullSearch.group(3)
    hjSearch = re.search(horseJockeySearchPattern, horseAndJockey)
    if hjSearch is None:
        print(horseAndJockey)
    out.append(hjSearch.group(1))
    out.append(hjSearch.group(2))

    for i in range(4,15):
        out.append(fullSearch.group(i))

    return out

def placeLengths(horseDicts, topItemsList):
    placeSegNames = ['placeSeg1','placeSeg2','placeSeg3','placeSeg4','placeSeg5','placeSeg6']
    lengthsSegNames = ['lengthsSeg1','lengthsSeg2','lengthsSeg3','lengthsSeg4','lengthsSeg5','lengthsSeg6']

    topItemsFull = False
    for items in topItemsList:
        if items[-1] != '':
            topItemsFull = True
            break

    #loop over the points of call of each race, looking at each horse in turn to determine if any have dropped out.
    #this is to ensure that the total number of horses in the race is known at each point of call.
    #this allows accurate placement of lengths for horses that were in last place at some point in the race.
    numHorses = []
    for seg in placeSegNames:
        tempNumHorses = len(horseDicts)
        for horseDict in horseDicts:
            if horseDict[seg] == '---': #if this horse was no longer in the race at this point of call
                tempNumHorses -= 1 #reduce horses in the race by one
        numHorses.append(str(tempNumHorses))

    horseCnt = 0
    for horseDict in horseDicts:
        if topItemsFull: #if all the points of call have lengths associated (i.e. one of them is not "start")
            startSeg = 0 #start placing lengths at the first point of call
        else:
            startSeg = 1 #otherwise, start at the second point of call (the first non-start point of call)

        numHorsesInd = 0
        segCnt = 0
        for seg in placeSegNames[startSeg:]:
            if horseDict[seg] != '---' and horseDict[seg] != numHorses[numHorsesInd] and horseDict[seg] != '' and horseDict[seg] != 'N/A':
                segCnt += 1
            numHorsesInd += 1

        nonBlankCnt = sum([1 for x in topItemsList[horseCnt] if x != ''])

        if segCnt - nonBlankCnt == 1:
            topItemsList[horseCnt][1:] = topItemsList[horseCnt][:-1]
            topItemsList[horseCnt][0] = horseDict['lastRacePlace']
        elif segCnt - nonBlankCnt == 2:
            topItemsList[horseCnt][2:] = topItemsList[horseCnt][:-2]
            topItemsList[horseCnt][0] = horseDict['lastRaceNum']
            topItemsList[horseCnt][1] = horseDict['lastRacePlace']
        
        horseCnt += 1
    
    ind = 0
    #loop over each point of call for each horse, inserting the appropriate lengths into the dataframe
    for horseDict in horseDicts:
        if topItemsFull: #if all the points of call have lengths associated (i.e. one of them is not "start")
            startSeg = 0 #start placing lengths at the first point of call
        else:
            startSeg = 1 #otherwise, start at the second point of call (the first non-start point of call)
        lengthsIndex = 0
        for segInd in range(startSeg, len(placeSegNames)):
            if horseDict[placeSegNames[segInd]] == numHorses[segInd]: #if horse was in last place at this point
                horseDict[lengthsSegNames[segInd]] = '' #lengths will be left blank
            else: 
                horseDict[lengthsSegNames[segInd]] = topItemsList[ind][lengthsIndex] #if not, fill in the lengths of the next point
                lengthsIndex += 1 #then go to next index in the lengths list
        ind += 1

    return horseDicts