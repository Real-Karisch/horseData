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

    firstPlaceItems = parseFirstPlace([betLines[i] for i in [betStartInd, betStartInd + 1]])
    secondPlaceitems = parseSecondPlace([betLines[i] for i in [betStartInd, betStartInd + 2]])
    thirdPlaceItems = parseThirdPlace([betLines[i] for i in [betStartInd, betStartInd + 3]])

    betDict['firstPlaceWin'] = firstPlaceItems[0]
    betDict['firstPlacePlace'] = firstPlaceItems[1]
    betDict['firstPlaceShow'] = firstPlaceItems[2]
    betDict['secondPlacePlace'] = secondPlaceitems[0]
    betDict['secondPlaceShow'] = secondPlaceitems[1]
    betDict['thirdPlaceShow'] = thirdPlaceItems[0]

    additionalLines = betLines[(betStartInd + 4):] + [firstPlaceItems[-1], secondPlaceitems[-1], thirdPlaceItems[-1]]

    index = 0
    for line in additionalLines:
        activeAdditional = parseAdditionalBetLines(line)
        keywordSearch = re.search('(Exacta|Trifecta|Superfecta|Daily Double)', activeAdditional[0])
        if keywordSearch is not None:
            keyword = keywordSearch.group(1).lower()
            print(line)
            betDict[keyword + 'Buyin'] = re.search('(\$\d\.\d\d)', activeAdditional[0]).group(1)
            betDict[keyword + 'Finish'] = activeAdditional[1]
            betDict[keyword + 'Payout'] = activeAdditional[2]
            betDict[keyword + 'Pool'] = activeAdditional[3]

    betDF = pd.DataFrame(betDict, index = [0])

    return betDF

def parseWPS(line):
    return 0

def parseFirstPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d)()() ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d) (\d?\d\.\d\d)() ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)
    else:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d) (\d?\d\.\d\d) (\d?\d\.\d\d) ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)

    out = []

    for i in range(1, 5):
        out.append(fullSearch.group(i))

    return out

def parseSecondPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None:
        fullSearch = re.search(r'\d?\d .+()() ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)
    elif labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d)() ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)
    else:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d) (\d?\d\.\d\d) ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)

    out = []

    for i in range(1, 4):
        out.append(fullSearch.group(i))

    return out

def parseThirdPlace(lines):
    header = lines[0]
    line = lines[1]

    labelSearch = re.search(r'Pgm Horse Win (Place)? ?(Show)?', header)
    if labelSearch.group(1) is None or labelSearch.group(2) is None:
        fullSearch = re.search(r'\d?\d .+() (?=\$\d\.\d\d)([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)
    else:
        fullSearch = re.search(r'\d?\d .+ (\d?\d\.\d\d) ([0-9.$ A-Za-z,]* [0-9-]* \d?\d?\d\.\d\d [0-9,]*)$', line)

    out = []

    for i in [1, 3]:
        out.append(fullSearch.group(i))

    return out

def parseAdditionalBetLines(line):

    fullSearch = re.search(r'([0-9.$ A-Za-z,]*) ([0-9-]*) (\d?\d?\d\.\d\d) ([0-9,]*)$', line)

    out = []

    for i in range(1,5):
        out.append(fullSearch.group(i))

    return out