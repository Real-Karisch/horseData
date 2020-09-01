import re
import pandas as pd
import os

def parseHorseInfo(horseLines):
    numHorses = int(len(horseLines) / 2)

    #set up empty df
    horseDF = pd.DataFrame(columns = ['lastRaceDay','lastRaceMonth','lastRaceYear','lastRaceTrack','lastRaceNum','lastRacePlace','program','horse', 'Jockey','weight','m_e','placePP','placeSeg1','lengthsSeg1','placeSeg2','lengthsSeg2','placeSeg3','lengthsSeg3','placeSeg4','lengthsSeg4','placeSeg5','lengthsSeg5','placeSeg6','lengthSeg6','odds','comments'])

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

    #loop over each horse in the lines provided
    for i in [x*2 for x in list(range(numHorses))]:
        activeHorse = horseLines[i:i+2]
        bottomItems = parseHorseBottomLine(activeHorse[1])
        topItems = parseHorseTopLine(activeHorse[0])

        horseDict['lastRaceDay'] = bottomItems[0]
        horseDict['lastRaceMonth'] = bottomItems[1]
        horseDict['lastRaceYear'] = bottomItems[2]
        horseDict['lastRaceTrack'] = bottomItems[3]
        horseDict['lastRaceNum'] = topItems[0]
        horseDict['lastRacePlace'] = topItems[1]
        horseDict['program'] = bottomItems[4]
        horseDict['horse'] = bottomItems[5]
        horseDict['jockey'] = bottomItems[6]
        horseDict['weight'] = bottomItems[7]
        horseDict['m_e'] = bottomItems[8]
        horseDict['placePP'] = bottomItems[9]
        horseDict['placeSeg1'] = bottomItems[10]
        horseDict['lengthsSeg1'] = topItems[2]
        horseDict['placeSeg2'] = bottomItems[11]
        horseDict['lengthsSeg2'] = topItems[3]
        horseDict['placeSeg3'] = bottomItems[12]
        horseDict['lengthsSeg3'] = topItems[4]
        horseDict['placeSeg4'] = bottomItems[13]
        horseDict['lengthsSeg4'] = topItems[5]
        horseDict['placeSeg5'] = bottomItems[14]
        horseDict['lengthsSeg5'] = topItems[6]
        horseDict['placeSeg6'] = bottomItems[15]
        horseDict['lengthsSeg6'] = topItems[7]
        horseDict['odds'] = bottomItems[16]
        horseDict['comments'] = bottomItems[17]

        activeDF = pd.DataFrame(horseDict, index = [0])
        
        horseDF = pd.concat([horseDF, activeDF])

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




##############################################################################################################

def parseFullDay(fullChart):
    newRaceInd = [-1] #first index will be 0 after conversion (controls for out of index error later)
    newRaceTest = 'Copyright 2020 Equibase Company LLC. All Rights Reserved.'
    for i in range(len(fullChart)):
        if re.search(newRaceTest, fullChart[i]) is not None: #check for the expression that signifies end of race
            newRaceInd.append(i)

    dayDF = pd.DataFrame(columns=['trackName','month','day','year','raceNum','distance','surface','segment1','segment2','segment3','segment4','segment5','segments',
        'lastRaceDay', 'lastRaceMonth', 'lastRaceYear', 'lastRaceTrack','lastRaceNum', 'lastRacePlace', 'program', 'horse', 'jockey', 'weight','m_e', 'placePP', 
        'placeSeg1', 'lengthsSeg1', 'placeSeg2','lengthsSeg2', 'placeSeg3', 'lengthsSeg3', 'placeSeg4', 'lengthsSeg4','placeSeg5', 'lengthsSeg5', 'placeSeg6',
        'lengthsSeg6', 'odds', 'comments'])

    for i in range(len(newRaceInd) - 1):

        raceDF = parseRace(fullChart[newRaceInd[i] + 1:newRaceInd[i + 1]])

        dayDF = pd.concat([dayDF, raceDF]) #loop over chunks of the file, each chunk representing a full race

    return dayDF

def parseRace(raceChart):

    cnt = 0

    raceDF = pd.DataFrame(columns=['trackName','month','day','year','raceNum','distance','surface','segment1','segment2','segment3','segment4','segment5','segments',
        'lastRaceDay', 'lastRaceMonth', 'lastRaceYear', 'lastRaceTrack','lastRaceNum', 'lastRacePlace', 'program', 'horse', 'jockey', 'weight','m_e', 'placePP', 
        'placeSeg1', 'lengthsSeg1', 'placeSeg2','lengthsSeg2', 'placeSeg3', 'lengthsSeg3', 'placeSeg4', 'lengthsSeg4','placeSeg5', 'lengthsSeg5', 'placeSeg6',
        'lengthsSeg6', 'odds', 'comments'])

    #loop to find indexes for different parse sections
    for line in raceChart:
        if re.search('Cancelled - ', line) is not None: #check for cancelled race first, if cancelled, return empty DF
            return raceDF
        elif re.search('- Quarter Horse', line) is not None: #also do not need to process quarter horses
            return raceDF
        elif re.search('Last Raced Pgm', line) is not None: #everything before this falls under "general info"
            genInd = cnt + 1
            horseInd = [cnt + 1]
        elif re.search('Fractional Times:|Final Time:', line) is not None: #after general info, need to process info for each horse
            horseInd.append(cnt)
            timesInd = [cnt]
        elif re.search('Run-Up: ', line) is not None: #after horses, timing and runup info
            timesInd.append(cnt + 1)
            betInd = [cnt + 1]
        elif re.search('Past Performance Running Line Preview', line) is not None: #after timing, betting info and additional horse info
            betInd.append(cnt)
            runLineInd = [cnt]
        elif re.search('Trainers: ', line) is not None: #finally, need to do trainers, owners and other ending info
            runLineInd.append(cnt)
            endInfoInd = cnt
        cnt += 1
    """
    print(raceChart[:genInd])
    print('++++++++++++++++++++++++++++++++++++')
    print(raceChart[horseInd[0]:horseInd[1]])
    print('++++++++++++++++++++++++++++++++++++')
    print(raceChart[timesInd[0]:timesInd[1]])
    print('++++++++++++++++++++++++++++++++++++')
    print(raceChart[betInd[0]:betInd[1]])
    print('++++++++++++++++++++++++++++++++++++')
    print(raceChart[runLineInd[0]:runLineInd[1]])
    print('++++++++++++++++++++++++++++++++++++')
    print(raceChart[endInfoInd:])
    """
    
    #genItems = parseGenInfo(raceChart[:genInd])
    horseItems = parseHorseInfo(raceChart[horseInd[0]:horseInd[1]])
    """
    timesItems = parseTimingInfo(raceChart[timesInd[0]:timesInd[1]])
    betItems = parseBetInfo(raceChart[betInd[0]:betInd[1]])
    runLineItems = parseRunLineInfo(raceChart[runLineInd[0]:runLineInd[1]])
    endItems = parseEndInfo(raceChart[endInfoInd:])
    """

    return horseItems
    #genDF = pd.DataFrame(horseItems)
    
    #return genDF

    #make df row, append to df, and return

with open('./charts/chartsTxt/eqbPDFChartPlus - 2020-08-11T010651.112.txt') as file:
    test1 = file.readlines()
with open('./charts/chartsTxt/eqbPDFChartPlus - 2020-08-11T010651.148.txt') as file:
    test2 = file.readlines()

parseFullDay(test1)
parseFullDay(test2)

