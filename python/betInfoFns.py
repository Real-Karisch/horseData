import re
import pandas as pd

def parseBetInfo(betLines):
    betDict = {}

    ind = 0
    for line in betLines:
        if re.search('Total WPS Pool', line) is not None:
            wpsInd = ind
        elif re.search('Pgm Horse Win', line) is not None:
            betStartInd = ind
        ind += 1

    wpsPool = parseWPS(betLines[wpsInd])
    firstPlaceItems = parseFirstPlace(betLines[betStartInd + 1])
    secondPlaceitems = parseSecondPlace(betLines[betStartInd + 2])
    thirdPlaceItems = parseThirdPlace(betLines[betStartInd + 3])

    betDict['wpsPool'] = wpsPool
    betDict['firstWinPayout'] = firstPlaceItems[0]

    additionalBetItems = []
    for line in betlines[(betStartInd + 4):]:
        additionalBetItems += parseAdditionalBetLines(line)

    

    #################### stopping here #########################
    return 0

def parseWPS(line):
    fullSearch = re.search(r'Total WPS Pool: \$([0-9,]+)', line)
    wpsPool = re.sub('[^0-9]', '', fullSearch.group(1))
    return wpsPool

def parseFirstPlace(line):
    return 0

def parseSecondPlace(line):
    return 0

def parseThirdPlace(line):
    return 0

def parseAdditionalBetLines(line):
    return 0