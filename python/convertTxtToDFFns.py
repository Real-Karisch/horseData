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
    newRaceInd = [0]
    newRaceTest = 'Copyright 2020 Equibase Company LLC. All Rights Reserved.'
    for i in range(len(fullChart)):
        if re.search(newRaceTest, fullChart[i]) is not None:
            newRaceInd.append(i + 1)

    dayDF = pd.DataFrame(columns=['trackName','month','day','year','raceNum','breed','distance','surface','segment1','segment2','segment3','segment4','segment5','segments'])

    for i in range(len(newRaceInd) - 1):

        raceDF = parseRace(fullChart[newRaceInd[i]:(min(newRaceInd[i+1], len(fullChart)))])
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
        elif re.search('Track *Record:', line) is not None:
            trackRecordInd = cnt
        elif re.search('Off *at:', line) is not None:
            genInd = cnt + 2
        elif re.search('Last *Raced *Pgm', line) is not None:
            horseInd = [cnt + 1]
        elif re.search('Fractional *Times:', line):
            horseInd.append(cnt)
            endInd = cnt
        cnt += 1
    """
    genItems = parseGenInfo(raceChart[:genInd], trackRecordInd=trackRecordInd)

    if genItems == 'Error':
        return 'Error - Quarter Horse'
    """
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

    #horseDF = pd.DataFrame(columns=)

    for i in [x*2 for x in range(horses)]:
        itemsTop = parseHorseTop(horseLines[i])
        itemsBottom = parseHorseBottom(horseLines[i+1])
    
    out = itemsTop + itemsBottom
    return out

def parseHorseTop(line):
    fullSearch = re.search(r' *(\d?\d) *(\d?\d) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *([A-Za-z0-9/]*) *', line)

    lastRaceNum = fullSearch.group(1)
    lastRacePlace = fullSearch.group(2)
    lengthsSeg1 = fullSearch.group(3)
    lengthsSeg2 = fullSearch.group(4)
    lengthsSeg3 = fullSearch.group(5)
    lengthsSeg4 = fullSearch.group(6)
    lengthsFin = fullSearch.group(7)

    out = [lastRaceNum, lastRacePlace, lengthsSeg1, lengthsSeg2, lengthsSeg3, lengthsSeg4, lengthsFin]
    return out

def parseHorseBottom(line):
    print(line)

    fullSearch = re.search(r'(\d?\d[A-Z][a-z]{2}\d\d *[A-Z]*|---) *(\d?\d) *([^0-9]+)(\d?\d?\d»?) *([A-Za-z0-9-]*) *(\d?\d) +(\d?\d) +(\d?\d)* *(\d?\d)* *(\d?\d)* *(\d?\d)* *(\d?\d)* *([0-9]+\.\d\d) *(.*)$', line)   
    
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


with open('./../charts/SUN-1.12.19.txt') as file:
    ex4 = file.readlines() #import another

test = parseFullDay(ex4)