import psycopg2
import psycopg2.extras
import os

from convertPDF.driver import parseFullDay

def generateEntries(txtFolderAddress):
    entries = {'races': [], 'horses': []}

    fileNames = os.listdir(txtFolderAddress)
    totalFiles = len(fileNames)
    print('Converting', totalFiles, 'files')
    fileCnt = 0

    alreadyPulled = []
    for fileName in fileNames:
        #if fileCnt > 600:
        #   print(fileName)
        if fileCnt % 300 == 0:
            print(fileCnt)
        fileCnt += 1

        with open(txtFolderAddress + '/' + fileName, encoding='cp1252') as file:
            chart = file.readlines()
            dayEntries = parseFullDay(chart)

        for raceEntries in dayEntries:
            if raceEntries == {}:
                continue

            racePk = (raceEntries['general']['trackName'], str(raceEntries['general']['month']) + '/' + str(raceEntries['general']['day']) + '/' + str(raceEntries['general']['year']), str(raceEntries['general']['raceNum']))
            if racePk in alreadyPulled:
                continue

            alreadyPulled.append(racePk)

            entries['races'].append(
                (
                    raceEntries['general']['trackName'],
                    str(raceEntries['general']['month']) + '/' + str(raceEntries['general']['day']) + '/' + str(raceEntries['general']['year']),
                    str(raceEntries['general']['raceNum']),
                    dictTry(raceEntries, ['general', 'stakes']),
                    dictTry(raceEntries, ['general', 'distance']),
                    dictTry(raceEntries, ['general', 'surface']),
                    dictTry(raceEntries, ['general', 'weather']),
                    dictTry(raceEntries, ['general', 'conditions']),
                    dictTry(raceEntries, ['general', 'startTime']),
                    dictTry(raceEntries, ['general', 'startNote']),
                    dictTry(raceEntries, ['general', 'segment1']),
                    dictTry(raceEntries, ['general', 'segment2']),
                    dictTry(raceEntries, ['general', 'segment3']),
                    dictTry(raceEntries, ['general', 'segment4']),
                    dictTry(raceEntries, ['general', 'segment5']),
                    dictTry(raceEntries, ['general', 'segments']),
                    dictTry(raceEntries, ['times', 'fracTime1']),
                    dictTry(raceEntries, ['times', 'fracTime2']),
                    dictTry(raceEntries, ['times', 'fracTime3']),
                    dictTry(raceEntries, ['times', 'fracTime4']),
                    dictTry(raceEntries, ['times', 'fracTime5']),
                    dictTry(raceEntries, ['times', 'finalTime']),
                    dictTry(raceEntries, ['times', 'runUp']),
                    dictTry(raceEntries, ['bet','wpsPool']),
                    dictTry(raceEntries, ['bet', 'firstPlaceWin']),
                    dictTry(raceEntries, ['bet', 'firstPlacePlace']),
                    dictTry(raceEntries, ['bet', 'firstPlaceShow']),
                    dictTry(raceEntries, ['bet', 'secondPlacePlace']),
                    dictTry(raceEntries, ['bet', 'secondPlaceShow']),
                    dictTry(raceEntries, ['bet', 'thirdPlaceShow']),
                    dictTry(raceEntries, ['bet', 'exactaBuyin']),
                    dictTry(raceEntries, ['bet', 'exactaFinish']),
                    dictTry(raceEntries, ['bet', 'exactaPayout']),
                    dictTry(raceEntries, ['bet', 'exactaPool']),
                    dictTry(raceEntries, ['bet','trifectaBuyin']),
                    dictTry(raceEntries, ['bet','trifectaFinish']),
                    dictTry(raceEntries, ['bet','trifectaPayout']),
                    dictTry(raceEntries, ['bet', 'trifectaPool']),
                    dictTry(raceEntries, ['bet','superfectaBuyin']),
                    dictTry(raceEntries, ['bet','superfectaFinish']),
                    dictTry(raceEntries, ['bet','superfectaPayout']),
                    dictTry(raceEntries, ['bet', 'superfectaPool']),
                    dictTry(raceEntries, ['bet','quinellaBuyin']),
                    dictTry(raceEntries, ['bet','quinellaFinish']),
                    dictTry(raceEntries, ['bet','quinellaPayout']),
                    dictTry(raceEntries, ['bet', 'quinellaPool']),
                )
            )

            cnt = 0
            for horse in raceEntries['horse']:
                program = horse['program']

                rlIndex = cnt
                rlCnt = 0
                for rlHorse in raceEntries['runline']:
                    if rlHorse['program'] == program:
                        rlIndex = rlCnt
                        break
                    rlCnt += 1

                trainerCnt = 0
                for trainerProgram in raceEntries['end'][0]['program']:
                    if trainerProgram == program:
                        trainer = raceEntries['end'][0]['trainer'][trainerCnt]
                        break
                    trainerCnt += 1

                ownerCnt = 0
                for ownerProgram in raceEntries['end'][1]['program']:
                    if ownerProgram == program:
                        owner = raceEntries['end'][1]['owner'][ownerCnt]
                        break
                    ownerCnt += 1

                entries['horses'].append(
                    (
                        raceEntries['general']['trackName'],
                        str(raceEntries['general']['month']) + '/' + str(raceEntries['general']['day']) + '/' + str(raceEntries['general']['year']),
                        raceEntries['general']['raceNum'],
                        horse['program'],
                        horse['horse'],
                        horse['lastRaceDay'],
                        horse['lastRaceMonth'],
                        horse['lastRaceYear'],
                        horse['lastRaceTrack'],
                        horse['jockey'],
                        horse['weight'],
                        horse['m_e'],
                        horse['placePP'],
                        dictTry(horse, ['placeSeg1']),
                        horse['placeSeg2'],
                        horse['placeSeg3'],
                        horse['placeSeg4'],
                        horse['placeSeg5'],
                        horse['placeSeg6'],
                        horse['odds'],
                        horse['comments'],
                        horse['lastRaceNum'],
                        horse['lastRacePlace'],
                        dictTry(horse, ['lengthsSeg1'], naFlag=False),
                        horse['lengthsSeg2'],
                        horse['lengthsSeg3'],
                        horse['lengthsSeg4'],
                        horse['lengthsSeg5'],
                        horse['lengthsSeg6'],
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg1'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg2'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg3'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg4'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg5'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlLengthsSeg6'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg1'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg2'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg3'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg4'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg5'], [rlIndex]),
                        dictTry(raceEntries, ['runline', 'rlPlaceSeg6'], [rlIndex]),
                        trainer,
                        owner
                    )
                )

                cnt += 1
    
    return entries

def populateDB(dbConnection, entries, schema='main'):
    populateRaces(dbConnection, entries['races'], schema)
    populateHorses(dbConnection, entries['horses'], schema)

def populateRaces(dbConnection, entries, schema='main'):
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            f"""
            INSERT INTO {schema}.races(
                track, 
                date,
                race,
                stakes,
                distance,
                surface,
                weather,
                conditions,
                "startTime",
                "startNote",
                segment1,
                segment2,
                segment3,
                segment4,
                segment5,
                segments,
                "fracTime1",
                "fracTime2",
                "fracTime3",
                "fracTime4",
                "fracTime5",
                "finalTime",
                runup,
                "wpsPool",
                "firstPlaceWin",
                "firstPlacePlace",
                "firstPlaceShow",
                "secondPlacePlace",
                "secondPlaceShow",
                "thirdPlaceShow",
                "exactaBuyin",
                "exactaFinish",
                "exactaPayout",
                "exactaPool",
                "trifectaBuyin",
                "trifectaFinish",
                "trifectaPayout",
                "trifectaPool",
                "superfectaBuyin",
                "superfectaFinish",
                "superfectaPayout",
                "superfectaPool",
                "quinellaBuyin",
                "quinellaFinish",
                "quinellaPayout",
                "quinellaPool"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            entries
        )

def populateHorses(dbConnection, entries, schema='main'):
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            f"""
            INSERT INTO {schema}.horses(
                track,
                date,
                race,
                "horseProgram",
                "horseName",
                "lastRaceDay",
                "lastRaceMonth",
                "lastRaceYear",
                "lastRaceTrack",
                jockey,
                weight,
                "ME",
                "placePP",
                "placeSeg1",
                "placeSeg2",
                "placeSeg3",
                "placeSeg4",
                "placeSeg5",
                "placeSeg6",
                odds,
                comments,
                "lastRaceNum",
                "lastRacePlace",
                "lengthsSeg1",
                "lengthsSeg2",
                "lengthsSeg3",
                "lengthsSeg4",
                "lengthsSeg5",
                "lengthsSeg6",
                "rlLengthsSeg1",
                "rlLengthsSeg2",
                "rlLengthsSeg3",
                "rlLengthsSeg4",
                "rlLengthsSeg5",
                "rlLengthsSeg6",
                "rlPlaceSeg1",
                "rlPlaceSeg2",
                "rlPlaceSeg3",
                "rlPlaceSeg4",
                "rlPlaceSeg5",
                "rlPlaceSeg6",
                trainer,
                owner
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s)
            """,
            entries
        )

def dictTry(dictionary, keys, listIndices=[], naFlag=True):
    thing = dict(dictionary)
    listIndex = 0
    dictIndex = 0
    for _ in range(len(keys) + len(listIndices)):
        if type(thing) == list:
            try:
                thing = thing[listIndices[listIndex]]
                listIndex += 1
            except IndexError:
                return 'N/A' if naFlag else ''
        else:
            try:
                thing = thing[keys[dictIndex]]
                dictIndex += 1
            except KeyError:
                return 'N/A' if naFlag else ''

    return thing

### DEBUG
if __name__ == '__main__':
    import json
    from usefulkarisch.fastFunctions import argParseDriver, parseStrToBool
    from dataClean.prepForSQL import prepEntriesForSQL

    args = argParseDriver(
        keywords=['schema', 'calculateEntries'],
        defaults={
            'schema': 'test',
            'calculateEntries': 'false'
        }
    )

    calculateEntries = parseStrToBool(args.calculateEntries)
    if calculateEntries:
        entries = generateEntries('C:/Users/jackk/Projects/horseData/charts/txts')
    else:
        with open('C:/Users/jackk/Projects/horseData/outputs/entries.json', 'r') as file:
            entries = json.loads(file.read())

    entries = prepEntriesForSQL(entries)

    conn = psycopg2.connect(
        host = "localhost",
        database = "horses",
        user = "karisch",
        password = "cocacola",
        port = 5432
    )

    populateDB(conn, entries, schema=args.schema)

    conn.commit()

    conn.close()