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
        raceDF = parseRace(fullChart[newRaceInd[i]:newRaceInd[i+1]])
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
            horseInd = [cnt]
        elif re.search('Fractional *Times:', line):
            horseInd.append(cnt)
            endInd = cnt
        cnt += 1

    genItems = parseGenInfo(raceChart[:genInd], trackRecordInd=trackRecordInd)

    if genItems == 'Error':
        return 'Error - Quarter Horse'
    #horseItems = parseHorseInfo(raceChart[horseInd[0]:horseInd[1]])
    #endItems = parseEndInfo(raceChart[endInd:])

    genDF = pd.DataFrame(genItems, index=[0])
    
    return genDF

    #make df row, append to df, and return