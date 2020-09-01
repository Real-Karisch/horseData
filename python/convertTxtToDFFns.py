import re
import pandas as pd
import os

from genInfoFns import parseGenInfo

def bulkTxtToDF(txtDir):
    if txtDir[-1] != '/':
        txtDir += '/'
    files = os.listdir(txtDir)

    for file in files:
        address = txtDir + file
        with open(address) as txtChart:
            fullChart = txtChart.readlines()
            fullDayDF = parseFullDay(fullChart)

    ## append full day df to running df and return

def parseFullDay(fullChart):
    newRaceInd = [-1] #first index will be 0 after conversion (controls for out of index error later)
    newRaceTest = 'Copyright 2020 Equibase Company LLC. All Rights Reserved.'
    for i in range(len(fullChart)):
        if re.search(newRaceTest, fullChart[i]) is not None: #check for the expression that signifies end of race
            newRaceInd.append(i)

    dayDF = pd.DataFrame(columns=['trackName','month','day','year','raceNum','breed','distance','surface','segment1','segment2','segment3','segment4','segment5','segments'])

    for i in range(len(newRaceInd) - 1):

        raceDF = parseRace(fullChart[newRaceInd[i] + 1:newRaceInd[i + 1]]) #loop over chunks of the file, each chunk representing a full race
        if type(raceDF) == str:
            continue
        else:
            dayDF = pd.concat([dayDF, raceDF])

    return dayDF

    ## append raceDF to running df and return

def parseRace(raceChart):

    cnt = 0

    for line in raceChart:
        if re.search('Cancelled *- *', line) is not None:
            return 'Error - cancelled'
        elif re.search('Track Record: (', line) is not None:
            trackRecordInd = cnt
        elif re.search('Off at: ', line) is not None:
            genInd = cnt + 2
        elif re.search('Last Raced Pgm', line) is not None:
            horseInd = [cnt + 1]
        elif re.search('Fractional Times:', line):
            horseInd.append(cnt)
            endInd = cnt
        cnt += 1
    
    genItems = parseGenInfo(raceChart[:genInd], trackRecordInd=trackRecordInd)

    if genItems == 'Error':
        return 'Error - Quarter Horse'
    
    if len(raceChart) < horseInd[1]:
        jack = 1
    horseItems = parseHorseInfo(raceChart[horseInd[0]:horseInd[1]])
    #endItems = parseEndInfo(raceChart[endInd:])

    genDF = pd.DataFrame(horseItems)
    
    return genDF

    #make df row, append to df, and return

def parseHorseInfo(horseLines):
    cnt = 0
    horses = int(len(horseLines) / 2)

    priorLine = 'bottom'
    #horseDF = pd.DataFrame(columns=)

    for line in horseLines:
        checkSearch = re.search(r'^ *\d?\d *[A-Z][a-z]{2}', line)
        if checkSearch is not None and priorLine == 'top':
            items = parseHorseBottom(line)
            priorLine = 'bottom'
        elif checkSearch is None:
            items = parseHorseTop(line)
            priorLine = 'top'
        else:
            items = parseHorseBoth(line)
            priorLine = 'both'
        
        if priorLine == 'top':
            itemsTop = items
        elif priorLine == 'bottom':
            itemsBottom = items
        else:
            itemsTop = items[:8]
            itemsBottom = items[8:]
    
    out = itemsTop + itemsBottom
    return out

def parseHorseTop(line):
    fullSearch = re.search(r' *(\d?\d) *(\d?\d) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *', line)

    lastRaceNum = fullSearch.group(1)
    lastRacePlace = fullSearch.group(2)
    lengthsSeg1 = fullSearch.group(3)
    lengthsSeg2 = fullSearch.group(4)
    lengthsSeg3 = fullSearch.group(5)
    lengthsSeg4 = fullSearch.group(6)
    lengthsSeg5 = fullSearch.group(7)
    lengthsFin = fullSearch.group(8)

    out = [lastRaceNum, lastRacePlace, lengthsSeg1, lengthsSeg2, lengthsSeg3, lengthsSeg4, lengthsSeg5, lengthsFin]
    return out

def parseHorseBottom(line):
    print(line)

    fullSearch = re.search(r'(\d?\d[A-Z][a-z]{2}\d\d *[A-Z]*|---) *(\d?\d) *([^0-9]+)(\d?\d?\d»?) *([A-Za-z0-9-]+ *[A-Za-z0-9-]*) *(\d?\d) +(\d?\d) +(\d?\d)* *(\d?\d)* *(\d?\d)* *(\d?\d)* *(\d?\d)* *([0-9]+\.\d\d) *(.*)$', line)   
    
    lastRaceDateTrack = fullSearch.group(1)
    program = fullSearch.group(2)
    horseAndJockey = fullSearch.group(3)
    weight = fullSearch.group(4)
    m_e = fullSearch.group(5)
    pp = fullSearch.group(6)
    seg1 = fullSearch.group(7)
    seg2 = fullSearch.group(8)
    seg3 = fullSearch.group(9)
    seg4 = fullSearch.group(10)
    seg5 = fullSearch.group(11)
    segFin = fullSearch.group(12)
    odds = fullSearch.group(13)
    comments = fullSearch.group(14)

    if re.search('-', lastRaceDateTrack) is not None:
        lastRaceDate = lastRaceDateTrack
        lastRaceTrack = lastRaceDateTrack
    else:
        dateTrackSearch = re.search(r'(\d?\d[A-Z][a-z]{2}\d\d) *([A-Z]*)', lastRaceDateTrack)
        lastRaceDate = dateTrackSearch.group(1)
        lastRaceTrack = dateTrackSearch.group(2)

    horseAndJockeySearch = re.search(r'([^0-9]*) *\(([A-Za-z., ]*)\) *$', horseAndJockey)
    horseName = re.sub(' ', '', horseAndJockeySearch.group(1))
    jockey = horseAndJockeySearch.group(2)

    out = [lastRaceDate,lastRaceTrack,program,horseName,jockey,weight,m_e,seg1,seg2,seg3,seg4,seg5,segFin,odds,comments]
    return out

def parseHorseBoth(line):
    fullSearch = re.search(r'(\d?\d[A-Z][a-z]{2}\d\d\d *[A-Z]*\d|---) *(\d?\d) *([^0-9]+)(\d?\d?\d»?) *([A-Za-z0-9-]*) *(\d?\d) +([^ ]*) +([^ ]*) *([^ ]*) *([^ ]*) *([^ ]*) *([^ ]*) *([0-9]+\.\d\d) *(.*)$', line)

    lastRaceDateTrack = fullSearch.group(1)

    program = fullSearch.group(2)
    horseAndJockey = fullSearch.group(3)
    weight = fullSearch.group(4)
    m_e = fullSearch.group(5)
    pp = fullSearch.group(6)
    seg1 = fullSearch.group(7)
    seg2 = fullSearch.group(8)
    seg3 = fullSearch.group(9)
    seg4 = fullSearch.group(10)
    seg5 = fullSearch.group(11)
    segFin = fullSearch.group(12)
    odds = fullSearch.group(13)
    comments = fullSearch.group(14)

    if re.search('-', lastRaceDateTrack) is not None:
        lastRaceNum = lastRaceDateTrack
        lastRacePlace = lastRaceDateTrack
        lastRaceDate = lastRaceDateTrack
        lastRaceTrack = lastRaceDateTrack
    else:
        dateTrackSearch = re.search(r'(\d?\d[A-Z][a-z]{2}\d\d)(\d) *([A-Z]*)(\d)', lastRaceDateTrack)
        lastRaceDate = dateTrackSearch.group(1)
        lastRaceNum = dateTrackSearch.group(2)
        lastRaceTrack = dateTrackSearch.group(3)
        lastRacePlace = dateTrackSearch.group(4)

    horseAndJockeySearch = re.search(r'([^0-9]*) *\(([A-Za-z., ]*)\) *$', horseAndJockey)
    horseName = re.sub(' ', '', horseAndJockeySearch.group(1))
    jockey = re.sub(' ', '',horseAndJockeySearch.group(2))

    lengthsSeg1 = 'n/a'
    lengthsSeg2 = 'n/a'
    lengthsSeg3 = 'n/a'
    lengthsSeg4 = 'n/a'
    lengthsSeg5 = 'n/a'
    lengthsFin = 'n/a'

    out = [lastRaceNum, lastRacePlace, lengthsSeg1, lengthsSeg2, lengthsSeg3, lengthsSeg4, lengthsSeg5, lengthsFin,lastRaceDate,lastRaceTrack,program,horseName,jockey,weight,m_e,seg1,seg2,seg3,seg4,seg5,segFin,odds,comments]

    return out

"""
with open('./../charts/SUN-1.12.19.txt') as file:
    ex4 = file.readlines() #import another

test = parseFullDay(ex4)
"""