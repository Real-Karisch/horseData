import re
import pandas as pd

from regexPatterns import *

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

    wpsInd = -1

    ind = 0
    for line in betLines:
        if re.search(WPSLinePattern, line) is not None:
            wpsInd = ind
        elif re.search(betsLinePattern, line) is not None:
            betStartInd = ind
        ind += 1

    if wpsInd == -1:
        print('No betting detected for race.')
        return {}
    
    linesCleaned = [x for x in betLines[betStartInd+1:] if re.search(r'^ (\d?\d[ABC]?|\$\d)', x) is not None]

    wpsPool = parseWPS(betLines[wpsInd])
    betDict['wpsPool'] = wpsPool

    firstPlaceItems = parseFirstPlace([betLines[betStartInd], linesCleaned[0]])
    secondPlaceItems = parseSecondPlace([betLines[betStartInd], linesCleaned[1]])
        

    betDict['firstPlaceWin'] = firstPlaceItems[0]
    betDict['firstPlacePlace'] = firstPlaceItems[1]
    betDict['firstPlaceShow'] = firstPlaceItems[2]
    betDict['secondPlacePlace'] = secondPlaceItems[0]
    betDict['secondPlaceShow'] = secondPlaceItems[1]

    if len(linesCleaned) > 2:
        thirdPlaceItems = parseThirdPlace([betLines[betStartInd], linesCleaned[2]])
        betDict['thirdPlaceShow'] = thirdPlaceItems[0]

        additionalLines = betLines[(betStartInd + 4):] + [firstPlaceItems[-1], secondPlaceItems[-1], thirdPlaceItems[-1]]

        for line in additionalLines:
            if line is None:
                line = ''

            keywordSearch = re.search(advancedBetsLinePattern, line)
            
            if keywordSearch is not None:
                keyword = re.sub(' ','',keywordSearch.group(1).lower())

                activeAdditional = parseAdditionalBetLines(line)

                betDict[keyword + 'Buyin'] = re.search(buyinPattern, activeAdditional[0]).group(1) if activeAdditional[0] != 'ERROR' else 'ERROR'
                betDict[keyword + 'Finish'] = activeAdditional[1]
                betDict[keyword + 'Payout'] = activeAdditional[3]
                betDict[keyword + 'Pool'] = activeAdditional[4]    

    return betDict

def parseWPS(line):
    fullSearch = re.search(WPSSearchPattern, line)

    return fullSearch.group(1)

def parseFirstPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(betLabelPattern, header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(firstPlaceWSearchPattern, line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(firstPlaceWPSearchPattern, line)
    else:
        fullSearch = re.search(firstPlaceWPSSearchPattern, line)

    out = []

    if fullSearch is None:
        print('Error in parseFirstPlace on line: ' + line)
        for _ in range(1, 5):
            out.append('ERROR')
    else:        
        for i in range(1, 5):
            out.append(fullSearch.group(i))

    return out

def parseSecondPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(betLabelPattern, header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(secondPlaceWSearchPattern, line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(secondPlaceWPSearchPattern, line)
    else:
        fullSearch = re.search(secondPlaceWPSSearchPattern, line)

    out = []
    if fullSearch is None:
        print('Error in parseSecondPlace on line: ' + line)
        for _ in range(1, 4):
            out.append('ERROR')
    else:        
        for i in range(1, 4):
            out.append(fullSearch.group(i))

    return out

def parseThirdPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(betLabelPattern, header)
    if labelSearch.group(1) is None or labelSearch.group(2) is None:
        fullSearch = re.search(thirdPlaceWPSearchPattern, line)
    else:
        fullSearch = re.search(thirdPlaceWPSSearchPattern, line)

    out = []

    if fullSearch is None:
        print('Error in parseThirdPlace on line: ' + line)
        for _ in range(1, 3):
            out.append('ERROR')
    else:        
        for i in range(1, 3):
            out.append(fullSearch.group(i))

    return out

def parseAdditionalBetLines(line):
    fullSearch = re.search(additionalBetLineSearchPattern, line)

    out = []

    if fullSearch is None:
        print('Error in parseAdditionalBetLines on line: ' + line)
        for _ in range(1, 6):
            out.append('ERROR')
    else:        
        for i in range(1, 6):
            out.append(fullSearch.group(i))

    return out