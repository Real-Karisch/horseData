import re

def getSecondsCountFromSegmentTime(segmentTimeStr):
    if segmentTimeStr is None:
        return None
    search = re.search((r'^(\d*):?(\d\d.\d\d)'), segmentTimeStr)
    if search is None:
        print(f"Search error in segment time conversion for {segmentTimeStr}")
        return None

    minutes = 0 if search.group(1) == "" else int(search.group(1))
    seconds = float(search.groups()[-1])
    return (minutes * 60) + seconds

def getCleanNumberFromStr(numberStr):
    if numberStr is None:
        return None
    return re.sub(r'[$,]', '', numberStr)

def formatHorseEntryForSQL(horseEntry):
    newHorseEntry = []
    for value in horseEntry:
        if value == "" or value == "N/A" or value == "ERROR" or value == "---" or value == '*':
            newHorseEntry.append(None)
        else:
            newHorseEntry.append(value)
    colNames = [
        'track',
        'date',
        'race',
        'horseProgram',
        'horseName',
        'lastRaceDay',
        'lastRaceMonth',
        'lastRaceYear',
        'lastRaceTrack',
        'jockey',
        'weight',
        'ME',
        'placePP',
        'placeSeg1',
        'placeSeg2',
        'placeSeg3',
        'placeSeg4',
        'placeSeg5',
        'placeSeg6',
        'odds',
        'comments',
        'lastRaceNum',
        'lastRacePlace',
        'lengthsSeg1',
        'lengthsSeg2',
        'lengthsSeg3',
        'lengthsSeg4',
        'lengthsSeg5',
        'lengthsSeg6',
        'rlLengthsSeg1',
        'rlLengthsSeg2',
        'rlLengthsSeg3',
        'rlLengthsSeg4',
        'rlLengthsSeg5',
        'rlLengthsSeg6',
        'rlPlaceSeg1',
        'rlPlaceSeg2',
        'rlPlaceSeg3',
        'rlPlaceSeg4',
        'rlPlaceSeg5',
        'rlPlaceSeg6',
        'trainer',
        'owner'
    ]
    entryDict = {colName: value for colName, value in zip(colNames, newHorseEntry)}
    return list(entryDict.values())

def formatRaceEntryForSQL(raceEntry):
    newRaceEntry = []
    for value in raceEntry:
        if value == "" or value == "N/A" or value == "ERROR":
            newRaceEntry.append(None)
        else:
            newRaceEntry.append(value)
    colNames = [
        'track',
        'date',
        'race',
        'stakes',
        'distance',
        'surface',
        'weather',
        'conditions',
        'startTime',
        'startNote',
        'segment1',
        'segment2',
        'segment3',
        'segment4',
        'segment5',
        'segments',
        'fracTime1',
        'fracTime2',
        'fracTime3',
        'fracTime4',
        'fracTime5',
        'finalTime',
        'runup',
        'wpsPool',
        'firstPlaceWin',
        'firstPlacePlace',
        'firstPlaceShow',
        'secondPlacePlace',
        'secondPlaceShow',
        'thirdPlaceShow',
        'exactaBuyin',
        'exactaFinish',
        'exactaPayout',
        'exactaPool',
        'trifectaBuyin',
        'trifectaFinish',
        'trifectaPayout',
        'trifectaPool',
        'superfectaBuyin',
        'superfectaFinish',
        'superfectaPayout',
        'superfectaPool',
        'quinellaBuyin',
        'quinellaFinish',
        'quinellaPayout',
        'quinellaPool'
    ]
    entryDict = {colName: value for colName, value in zip(colNames, newRaceEntry)}
    entryDict['fracTime1'] = getSecondsCountFromSegmentTime(entryDict['fracTime1'])
    entryDict['fracTime2'] = getSecondsCountFromSegmentTime(entryDict['fracTime2'])
    entryDict['fracTime3'] = getSecondsCountFromSegmentTime(entryDict['fracTime3'])
    entryDict['fracTime4'] = getSecondsCountFromSegmentTime(entryDict['fracTime4'])
    entryDict['fracTime5'] = getSecondsCountFromSegmentTime(entryDict['fracTime5'])
    entryDict['finalTime'] = getSecondsCountFromSegmentTime(entryDict['finalTime'])
    entryDict['wpsPool'] = getCleanNumberFromStr(entryDict['wpsPool'])
    entryDict['exactaBuyin'] = getCleanNumberFromStr(entryDict['exactaBuyin'])
    entryDict['exactaPayout'] = getCleanNumberFromStr(entryDict['exactaPayout'])
    entryDict['exactaPool'] = getCleanNumberFromStr(entryDict['exactaPool'])
    entryDict['trifectaBuyin'] = getCleanNumberFromStr(entryDict['trifectaBuyin'])
    entryDict['trifectaPayout'] = getCleanNumberFromStr(entryDict['trifectaPayout'])
    entryDict['trifectaPool'] = getCleanNumberFromStr(entryDict['trifectaPool'])
    entryDict['superfectaBuyin'] = getCleanNumberFromStr(entryDict['superfectaBuyin'])
    entryDict['superfectaPayout'] = getCleanNumberFromStr(entryDict['superfectaPayout'])
    entryDict['superfectaPool'] = getCleanNumberFromStr(entryDict['superfectaPool'])
    entryDict['quinellaBuyin'] = getCleanNumberFromStr(entryDict['quinellaBuyin'])
    entryDict['quinellaPayout'] = getCleanNumberFromStr(entryDict['quinellaPayout'])
    entryDict['quinellaPool'] = getCleanNumberFromStr(entryDict['quinellaPool'])
    return list(entryDict.values())

def prepEntriesForSQL(entries):
    entries['horses'] = [formatHorseEntryForSQL(x) for x in entries['horses']]
    entries['races'] = [formatRaceEntryForSQL(x) for x in entries['races']]
    return entries

if __name__ == '__main__':
    import json

    with open('C:/Users/jackk/Projects/horseData/outputs/entries.json', 'r') as file:
        entries = json.loads(file.read())
    entries['races'] = [formatRaceEntryForSQL(x) for x in entries['races']]