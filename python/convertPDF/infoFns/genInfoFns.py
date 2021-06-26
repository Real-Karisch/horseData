import re
import pandas as pd

from .regexPatterns import *

def parseGenInfo(genLines):

    dfDict = {}
    
    dfDict['trackName'], dfDict['month'], dfDict['day'], dfDict['year'], dfDict['raceNum'] = parseLine1(genLines[0])
    dfDict['stakes'] = parseLine2(genLines[1])
    
    for line in genLines[0:]:
        if re.search(distanceSurfaceLinePattern, line) is not None:
            dfDict['distance'], dfDict['surface'] = parseDistanceSurface(line)
        elif re.search(weatherConditionsLinePattern, line) is not None:
            dfDict['weather'], dfDict['conditions'] = parseWeatherConditions(line)
        elif re.search(startNotesLinePattern, line) is not None:
            dfDict['startTime'], dfDict['startNote'] = parseStart(line)
        elif re.search(segmentsLinePattern, line) is not None:
            dfDict['segment1'], dfDict['segment2'], dfDict['segment3'], dfDict['segment4'], dfDict['segment5'] = parseSegments(line)

    if dfDict['segment3'] == '':
        dfDict['segments'] = 2
    elif dfDict['segment4'] == '':
        dfDict['segments'] = 3
    elif dfDict['segment5'] == '':
        dfDict['segments'] = 4
    else:
        dfDict['segments'] = 5

    return dfDict

def parseLine1(line):
    simpleLine = re.sub(r'[^-A-Za-z]', '', line)

    if re.search(r'(RMTC|CALLAWAYGARDEN)', simpleLine) is not None: #check if track is lethbridge
        fullSearch = re.search(genInfoLine1LethbridgePattern, line)
    else:
        fullSearch = re.search(genInfoLine1TrackPattern, line)

    trackNameRaw = fullSearch.group(1)
    dateRaw = fullSearch.group(2)
    raceNumRaw = fullSearch.group(3)

    #track name -> abbreviated name
    trackNameFull = re.sub('[^A-Za-z ]', '', trackNameRaw)
    trackName = trackLongToShort[trackNameFull]

    #date
    dateSearch = re.search(genInfoLine1DatePattern, dateRaw)
    monthRaw = dateSearch.group(1)
    month = monthNameToNumber[monthRaw]
    day = dateSearch.group(2)
    year = dateSearch.group(3)

    #race number
    raceNum = re.search(genInfoLine1RaceNumPattern, raceNumRaw).group(0)

    out = [trackName, int(month), int(day), int(year), int(raceNum)]

    return out

def parseLine2(line):
    breedRaw = re.search(genInfoLine2BreedPattern, line).group(1)
    stakes = ''
    if re.search(stakesLinePattern, line) is not None:
        stakesSearch = re.search(gradePattern, line)
        if stakesSearch is None:
            stakes = 'General'
        else:
            stakes = stakesSearch.group(1)
    breed = re.sub('[^A-Za-z]', '', breedRaw)
    return stakes

def parseDistanceSurface(line):
    fullSearch = re.search(distanceSurfaceFullSearchPattern, line)
    if fullSearch is None:
        specSearch = re.match(distanceSurfaceSpecSearchPattern, line)
    else:
        specSearch = re.match(distanceSurfaceSpecSearchPattern, fullSearch.group(0))

    if specSearch is None:
        print('Match error in parseDistanceSurface on line: ' + line)
        return ['ERROR', 'ERROR']

    distance, surface = [specSearch.group(1).strip(), specSearch.group(2).strip()]

    if re.search('- Originally', surface) is not None:
        surface = re.search(r'([A-Za-z ]+)-', surface).group(1).strip()

    surface = re.sub(r' Current', '', surface)

    out = [distance, surface]

    return out

def parseWeatherConditions(line):
    fullSearch = re.search(weatherConditionsSearchPattern, line)

    if fullSearch is None:
        print('Match error in parseWeatherConditions on line: ' + line)
        return ['ERROR'] * 2

    weather = fullSearch.group(1)
    conditions = fullSearch.group(2)

    out = [weather, conditions]

    return out

def parseStart(line):
    fullSearch = re.search(startNotesSearchPattern, line)

    if fullSearch is None:
        print('Match error in parseStart on line: ' + line)
        return ['ERROR'] * 2

    startTime = fullSearch.group(1)
    startNote = fullSearch.group(2)

    out = [startTime, startNote]

    return out

def parseSegments(line):
    fullSearch = re.search(segmentsSearchPattern, line)
    segment1 = fullSearch.group(1)
    segment2 = fullSearch.group(2)
    segment3 = fullSearch.group(3)
    segment4 = fullSearch.group(4)
    segment5 = fullSearch.group(5)

    return [segment1, segment2, segment3, segment4, segment5]

trackLongToShort = {}
trackShortToLong = {}
tracksDF = pd.read_csv('./../excel/tracks.csv', delimiter=',', header=None)
for i in range(tracksDF.shape[0]):
    trackLongToShort[tracksDF.iloc[i,1]] = tracksDF.iloc[i,0]
    trackShortToLong[tracksDF.iloc[i,0]] = tracksDF.iloc[i,1]

monthNameToNumber = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}