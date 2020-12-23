import re
import pandas as pd

"""
This file contains functions that are called in order to parse the lines of the chart relating to betting info.
"""

def parseBetInfo(betLines):
    """
    Driver function to manage/delegate parsing of bet lines and generating dictionaries with info.
    Input: betLines, a list of strings, each string containing one line of the race chart
    Output: a dictionary containing 
    """
    betDict = {}

    ind = 0
    for line in betLines:
        if re.search('Total WPS Pool', line) is not None:
            wpsInd = ind
        elif re.search('Pgm Horse Win', line) is not None:
            betStartInd = ind
        ind += 1
    
    linesCleaned = [x for x in betLines[betStartInd+1:] if re.search(r'^ (\d?\d[ABC]?|\$\d)', x) is not None]

    wpsPool = parseWPS(betLines[wpsInd])
    betDict['wpsPool'] = wpsPool

    firstPlaceItems = parseFirstPlace([betLines[betStartInd], linesCleaned[0]])
    secondPlaceItems = parseSecondPlace([betLines[betStartInd], linesCleaned[1]])
    thirdPlaceItems = parseThirdPlace([betLines[betStartInd], linesCleaned[2]])

    betDict['firstPlaceWin'] = firstPlaceItems[0]
    betDict['firstPlacePlace'] = firstPlaceItems[1]
    betDict['firstPlaceShow'] = firstPlaceItems[2]
    betDict['secondPlacePlace'] = secondPlaceItems[0]
    betDict['secondPlaceShow'] = secondPlaceItems[1]
    betDict['thirdPlaceShow'] = thirdPlaceItems[0]

    additionalLines = betLines[(betStartInd + 4):] + [firstPlaceItems[-1], secondPlaceItems[-1], thirdPlaceItems[-1]]

    index = 0
    for line in additionalLines:
        if line is None:
            line = ''

        keywordSearch = re.search('(Exacta|Trifecta|Superfecta|Daily Double)', line)
        
        if keywordSearch is not None:
            keyword = re.sub(' ','',keywordSearch.group(1).lower())

            activeAdditional = parseAdditionalBetLines(line)

            betDict[keyword + 'Buyin'] = re.search('(\$\d\.\d\d)', activeAdditional[0]).group(1)
            betDict[keyword + 'Finish'] = activeAdditional[1]
            betDict[keyword + 'Payout'] = activeAdditional[3]
            betDict[keyword + 'Pool'] = activeAdditional[4]

    betDF = pd.DataFrame(betDict, index = [0])

    return betDF

def parseWPS(line):
    fullSearch = re.search(r'Total WPS Pool: \$([0-9,]*)', line)

    return fullSearch.group(1)

def parseFirstPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d)()()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d) (\d?\d\.\d\d)()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)
    else:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d) (\d?\d\.\d\d) (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)

    out = []

    for i in range(1, 5):
        out.append(fullSearch.group(i))

    return out

def parseSecondPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(r'\d?\d[ABC]? .+()()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d)()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)
    else:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d) (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)

    if fullSearch is None:
        print(lines)
    out = []

    for i in range(1, 4):
        out.append(fullSearch.group(i))

    return out

def parseThirdPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None or labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d[ABC]? .+()( (?=\$\d\.\d\d)([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\)? )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)
    else:
        fullSearch = re.search(r'\d?\d[ABC]? .+ (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\)? )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$', line)

    out = []

    if fullSearch is None:
        print(lines[1])

    for i in range(1,3):
        out.append(fullSearch.group(i))

    return out

def parseAdditionalBetLines(line):

    fullSearch = re.search(r'([0-9.$ A-Za-z,]*) ([0-9-/ABC]*) (\([0-9A-Za-z ]+\) )?([0-9,.]+\.\d\d) ([0-9,.]*)( [0-9,.]*)?$', line)

    out = []

    for i in range(1,6):
        out.append(fullSearch.group(i))

    return out