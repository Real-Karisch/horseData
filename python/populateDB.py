import psycopg2
import psycopg2.extras
import os

from convertPDF.driver import parseFullDay

def generateEntries(txtFolderAddress):
    entries = {'races': [], 'horses': []}

    fileNames = os.listdir(txtFolderAddress)
    for fileName in fileNames:
        with open(txtFolderAddress + '/' + fileName) as file:
            chart = file.readlines()
            dayEntries = parseFullDay(chart)

        for raceEntries in dayEntries:
            if raceEntries == {}:
                continue

            entries['races'].append(
                (
                    raceEntries['general']['trackName'],
                    str(raceEntries['general']['month']) + '/' + str(raceEntries['general']['day']) + '/' + str(raceEntries['general']['year']),
                    str(raceEntries['general']['raceNum']),
                    raceEntries['general']['distance'],
                    raceEntries['general']['surface'],
                    raceEntries['general']['weather'],
                    raceEntries['general']['conditions'],
                    raceEntries['general']['startTime'],
                    raceEntries['general']['startNote'],
                    raceEntries['general']['segment1'],
                    raceEntries['general']['segment2'],
                    raceEntries['general']['segment3'],
                    raceEntries['general']['segment4'],
                    raceEntries['general']['segment5'],
                    raceEntries['general']['segments'],
                    raceEntries['times']['fracTime1'],
                    raceEntries['times']['fracTime2'],
                    raceEntries['times']['fracTime3'],
                    raceEntries['times']['fracTime4'],
                    raceEntries['times']['fracTime5'],
                    raceEntries['times']['finalTime'],
                    raceEntries['times']['runUp'],
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
                    dictTry(raceEntries, ['bet', 'trifectaPool'])
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

def populateDB(dbConnection, entries):
    populateRaces(dbConnection, entries['races'])
    populateHorses(dbConnection, entries['horses'])

def populateRaces(dbConnection, entries):
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO main.races(
                track, 
                date,
                race,
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
                "trifectaPool"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s)
            """,
            entries
        )

def populateHorses(dbConnection, entries):
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO main.horses(
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