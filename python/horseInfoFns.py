import re
import pandas as pd

def parseHorseInfo(horseLines):
    numHorses = int(len(horseLines) / 2)

    #set up empty df
    horseDF = pd.DataFrame(columns = ['lastRaceDay','lastRaceMonth','lastRaceYear','lastRaceTrack','lastRaceNum','lastRacePlace','program','horse', 'jockey','weight','m_e','placePP','placeSeg1','lengthsSeg1','placeSeg2','lengthsSeg2','placeSeg3','lengthsSeg3','placeSeg4','lengthsSeg4','placeSeg5','lengthsSeg5','placeSeg6','lengthsSeg6','odds','comments'])

    horseDict = {}

    priorLineBottom = True
    missingTopLineInd = []
    for i in range(len(horseLines)): #loop to add spacing if top line missing (can only happen if horse has never been raced AND was in last place the whole race)
        line = horseLines[i]
        if re.search('^ (\d?\d[A-Z][a-z]{2}\d\d|---)', line) is not None and priorLineBottom: #check to see if the current line is bottom and the last line was also bottom
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
        horseDict['horse'] = bottomItems[5]
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
        else:
            horseDict['lastRaceNum'] = topItems[0]
            horseDict['lastRacePlace'] = topItems[1]
            topItemsList.append(topItems[2:])

        activeDF = pd.DataFrame(horseDict, index = [0])
        
        horseDF = pd.concat([horseDF, activeDF])

    horseDF.reset_index(drop = True, inplace=True)
    
    horseDF = placeLengths(horseDF, topItemsList)

    return horseDF

def parseHorseTopLine(line):
    fullSearch = re.search(r'^ ([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*)', line)

    out = []
    for i in range(1,9):
        out.append(fullSearch.group(i))

    return out

def parseHorseBottomLine(line):
    fullSearch = re.search(r'^ (\d?\d[A-Z][a-z]{2}\d\d [A-Z]{2,3}|---) (\d?\d) ([^0-9]+) (\d?\d?\d)[»½]* ([A-Za-z -]*\d?) ([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ([0-9]+\.\d\d)\*? (.*)$', line)

    out = []
    dateSearch = re.search(r'(\d?\d)([A-Z][a-z]{2})(\d\d) ([A-Z]{2,3})', fullSearch.group(1))
    if dateSearch is not None:
        out[:4] = [dateSearch.group(1), dateSearch.group(2), dateSearch.group(3), dateSearch.group(4)]
    else:
        out[:4] = [''] * 4
    
    out.append(fullSearch.group(2))

    horseAndJockey = fullSearch.group(3)
    hjSearch = re.search(r'(.*) \(([-A-Za-z,. ]+)\)', horseAndJockey)
    out.append(hjSearch.group(1))
    out.append(hjSearch.group(2))

    for i in range(4,15):
        out.append(fullSearch.group(i))

    return out

def placeLengths(horseDF, topItemsList):
    placeSegNames = ['placeSeg1','placeSeg2','placeSeg3','placeSeg4','placeSeg5','placeSeg6']
    lengthsSegNames = ['lengthsSeg1','lengthsSeg2','lengthsSeg3','lengthsSeg4','lengthsSeg5','lengthsSeg6']

    numHorses = []
    for seg in placeSegNames:
        tempNumHorses = horseDF.shape[0]
        for i in range(horseDF.shape[0]):
            if horseDF[seg][i] == '---':
                tempNumHorses -= 1
        numHorses.append(str(tempNumHorses))
        
    for horseInd in range(horseDF.shape[0]):
        lengthsIndex = 0
        for segInd in range(len(placeSegNames)):
            if horseDF[placeSegNames[segInd]][horseInd] == numHorses[segInd]: #if horse was in last place at this point
                horseDF.loc[horseInd, lengthsSegNames[segInd]] = '' #lengths will be left blank
            else: 
                horseDF.loc[horseInd, lengthsSegNames[segInd]] = topItemsList[horseInd][lengthsIndex] #if not, fill in the lengths of the next point
                lengthsIndex += 1 #then go to next index in the lengths list

    return horseDF