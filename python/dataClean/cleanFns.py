import pandas as pd
import numpy as np
import re

def racesClean(racesdf):
    outdf = racesdf.loc[racesdf['fracTime1'] != 'ERROR'].reset_index(drop=True).copy()

    outdf.loc[:, 'startTime'] = pd.to_datetime(outdf.loc[:, 'date'] + ' ' + outdf.loc[:, 'startTime'])
    outdf.loc[:, 'date'] = pd.to_datetime(outdf['date'])
    outdf.loc[:, 'race'] = pd.to_numeric(outdf['race'])
    
    outdf.loc[:, 'wpsPool'] = outdf['wpsPool'].str.replace(',', '')
    outdf = numClean(outdf, 'wpsPool')

    outdf = numClean(outdf, 'firstPlaceWin')
    outdf = numClean(outdf, 'firstPlacePlace')
    outdf = numClean(outdf, 'firstPlaceShow')
    outdf = numClean(outdf, 'secondPlacePlace')
    outdf = numClean(outdf, 'secondPlaceShow')
    outdf = numClean(outdf, 'thirdPlaceShow')
    outdf = numClean(outdf, 'runup')

    outdf.loc[:, 'exactaPool'] = outdf['exactaPool'].str.replace(',', '')
    outdf.loc[:, 'exactaPool'] = outdf['exactaPool'].str.extract('(\d+)\.?')
    outdf = numClean(outdf, 'exactaPool')
    outdf.loc[:, 'trifectaPool'] = outdf['trifectaPool'].str.replace(',', '')
    outdf.loc[:, 'trifectaPool'] = outdf['trifectaPool'].str.extract('(\d+)\.?')
    outdf = numClean(outdf, 'trifectaPool')
    outdf.loc[:, 'exactaPayout'] = outdf['exactaPayout'].str.replace(',', '')
    outdf.loc[:, 'exactaPayout'] = outdf['exactaPayout'].str.extract('(\d+)\.?')
    outdf = numClean(outdf, 'exactaPayout')
    outdf.loc[:, 'trifectaPayout'] = outdf['trifectaPayout'].str.replace(',', '')
    outdf.loc[:, 'trifectaPayout'] = outdf['trifectaPayout'].str.extract('(\d+)\.?')
    outdf = numClean(outdf, 'trifectaPayout')
    
    outdf.loc[:, 'distance'] = pd.Series([0] * outdf.shape[0])

    for distanceKey, distanceValue in distanceDict.items():
        outdf.loc[outdf['distanceStr'] == distanceKey, 'distance'] = distanceValue

    columns = list(outdf.columns)
    distanceStrInd = columns.index('distanceStr')
    columns.insert(distanceStrInd + 1, columns.pop(-1))

    outdf = outdf[columns]

    for i in range(1, 7):
        colName = 'finalTime' if i == 6 else 'fracTime' + str(i)
        onlyPos = outdf.loc[~(outdf[colName].isnull()), colName]
        convTime = onlyPos.str.extract(r'^(\d?):?(\d\d\.\d\d)')
        convTime.loc[convTime[0].isnull(), 0] = '1'
        convTime.loc[convTime[1].isnull(), 1] = '0'
        convTime.loc[convTime[0] == '', 0] = '0'
        convTime = convTime.astype({0: 'float', 1: 'float'})
        convTime.loc[:, 0] = convTime[0] * 60
        convTime = convTime.sum(1)
        outdf.loc[outdf[colName].isnull(), colName] = '-1'
        outdf.loc[convTime.index, colName] = convTime.astype('string')
        outdf.loc[:, colName] = outdf[colName].astype('float')
        outdf.loc[outdf[colName] == -1, colName] = np.nan
        
        if i == 6:
            break

        outdf.loc[outdf['segment' + str(i)].isnull(), 'segment' + str(i)] = ''

        for segKey, segVal in segmentDict.items():
            outdf.loc[outdf['segment' + str(i)] == segKey, 'segment' + str(i)] = str(segVal)

        outdf.sort_index(inplace=True)

    return outdf

def horsesClean(horsesdf):
    outdf = horsesdf.copy()

    outdf.loc[:, 'date'] = pd.to_datetime(outdf['date'])
    outdf.loc[:, 'race'] = pd.to_numeric(outdf['race'])

    outdf = numClean(outdf, 'lastRaceDay')
    outdf = numClean(outdf, 'lastRaceYear')
    outdf = numClean(outdf, 'weight')
    outdf = numClean(outdf, 'placePP')
    outdf = numClean(outdf, 'odds')

    tracks = pd.read_csv('./../excel/tracks.csv')
    trackAbbreves = list(tracks['shortName'])
    indices = outdf['lastRaceTrack'].copy()

    for abbreve in trackAbbreves:
        indices[indices == abbreve] = '-1'

    indices = indices[indices != '-1']
    outdf.loc[indices.index, 'lastRaceNum'] = ''
    outdf.loc[indices.index, 'lastRacePlace'] = ''

    outdf = numClean(outdf, 'lastRaceNum')
    outdf = numClean(outdf, 'lastRacePlace')

    for i in range(1, 7):
        outdf.loc[outdf['placeSeg' + str(i)] == '---', 'placeSeg' + str(i)] = ''
        outdf.loc[outdf['placeSeg' + str(i)] == '*', 'placeSeg' + str(i)] = ''
        outdf = numClean(outdf, 'placeSeg' + str(i))
        outdf.loc[outdf['lengthsSeg' + str(i)] == '---', 'lengthsSeg' + str(i)] = ''
        outdf.loc[outdf['lengthsSeg' + str(i)] == '*', 'lengthsSeg' + str(i)] = ''
        outdf = lengthsParse(outdf, 'lengthsSeg' + str(i))
        outdf.loc[outdf['rlPlaceSeg' + str(i)] == '---', 'rlPlaceSeg' + str(i)] = ''
        outdf.loc[outdf['rlPlaceSeg' + str(i)] == '*', 'rlPlaceSeg' + str(i)] = ''
        outdf = numClean(outdf, 'rlPlaceSeg' + str(i))
        outdf.loc[outdf['rlLengthsSeg' + str(i)] == '---', 'rlLengthsSeg' + str(i)] = ''
        outdf.loc[outdf['rlLengthsSeg' + str(i)] == '*', 'rlLengthsSeg' + str(i)] = ''
        outdf = lengthsParse(outdf, 'rlLengthsSeg' + str(i))

    return outdf

def numClean(df, colName):
    df.loc[df[colName].isnull(), colName] = '-1'
    df.loc[df[colName] == 'ERROR', colName] = '-1'
    df.loc[df[colName] == '', colName] = '-1'
    df.loc[:, colName] = pd.to_numeric(df[colName])
    df.loc[df[colName] == -1, colName] = np.nan
    return df

def lengthsParse(df, colName):
    df.loc[df[colName] == 'Nose', colName] = '0.1'
    df.loc[df[colName] == 'Head', colName] = '0.2'
    df.loc[df[colName] == 'Neck', colName] = '0.3'
    df.loc[df[colName].isnull(), colName] = '-1'
    df.loc[df[colName].str.contains('[A-Z]'), colName] = '0.1'

    regNums = df.loc[df[colName].str.contains(r'\d?\d'), colName]

    slashes = df.loc[df[colName].str.contains(r'/'), colName]
    slashesSplit = slashes.str.extract('(\d?\d?)(\d)/(\d)')
    slashesSplit.loc[slashesSplit[0] == '', 0] = '0'
    slashesSplit = slashesSplit.astype({0: 'int', 1: 'int', 2: 'int'})
    slashesSplit['fractions'] = slashesSplit[1] / slashesSplit[2]
    combined = (slashesSplit[0] + slashesSplit['fractions']).astype('str')

    df.loc[regNums.index, colName] = regNums
    df.loc[combined.index, colName] = combined
    df.loc[:, colName] = pd.to_numeric(df[colName])
    df.loc[df[colName] == -1, colName] = np.nan

    return df

distanceDict = {
    'One Furlong': 1.0,
    'Two Furlongs': 2.0,
    'Two And One Half Furlongs': 2.5,
    'Three Furlongs': 3.0,
    'Three And One Half Furlongs': 3.5,
    'Four Furlongs': 4.0,
    'Four And One Half Furlongs': 4.5,
    'Five Furlongs': 5.0,
    'Five And One Fourth Furlongs': 5.25,
    'Five And One Half Furlongs': 5.5,
    'Six Furlongs': 6.0,
    'Six And One Half Furlongs': 6.5,
    'Seven Furlongs': 7.0,
    'Seven And One Half Furlongs': 7.5,
    'One Mile': 8.0,
    'One Mile And Forty Yards': 8.181818,
    'One Mile And Seventy Yards': 8.318181,
    'One And One Sixteenth Miles': 8.5,
    'One And One Eighth Miles': 9.0,
    'One And Three Sixteenth Miles': 9.5,
    'One And One Fourth Miles': 10.0,
    'One And Five Sixteenth Miles': 10.5,
    'One And Three Eighth Miles': 11.0,
    'One And Seven Sixteenth Miles': 11.5,
    'One And One Half Miles': 12.0,
    'One And Nine Sixteenth Miles': 12.5,
    'One And Five Eighth Miles': 13.0,
    'One and Eleven Sixteenth Miles': 13.5,
    'One And Three Fourth Miles': 14.0,
    'One And Thirteen Sixteenth Miles': 14.5,
    'One And Seven Eighth Miles': 15.0,
    'One And Fifteen Sixteenth Miles': 15.5,
    'Two Miles': 16.0,
    'Two Miles And Seventy Yards': 16.318181,
    'Two And One Sixteenth Miles': 16.5,
    'Two And One Eighth Miles': 17.0,
    'Two And Three Sixteenth Miles': 17.5,
    'Two And One Fourth Miles': 18.0,
    'Two And Five Sixteenth Miles': 18.5,
    'Two And Three Eighth Miles': 19.0,
    'Two And Seven Sixteenth Miles': 19.5,
    'Two And One Half Miles': 20.0,
    'Two And Nine Sixteenth Miles': 20.5,
    'Two And Five Eighth Miles': 21.0,
    'Two And Eleven Sixteenth Miles': 21.5,
    'Two And Three Fourth Miles': 22.0,
    'Two And Thirteen Sixteenth Miles': 22.5,
    'Two And Seven Eighth Miles': 23.0,
    'Two And Fifteen Sixteenth Miles': 23.5,
    'Three Miles': 24.0,
    'Three And One Eighth Miles': 25.0,
    'Three And One Fourth Miles': 26.0,
    'Two And Three Eighth Miles': 27.0,
    'Three And One Half Miles': 28.0,
    'Three And Five Eighth Miles': 29.0,
    'Three And Three Fourth Miles': 30.0,
    'Three And Seven Eighth Miles': 31.0,
    'Four Miles': 32.0,
    }

segmentDict = {
    '3/16': 1.5,
    '1/4': 2.0,
    '3/8': 3.0,
    '1/2': 4.0,
    '5/8': 5.0,
    '3/4': 6.0,
    '7/8': 7.0,
    '1m': 8.0,
    '11/8': 9.0,
    '11/4': 10.0,
    '13/8': 11.0,
    '11/2': 12.0,
    '15/8': 13.0,
    '13/4': 14.0,
    '17/8': 15.0,
    '2m': 16.0,
    '21/4': 18.0,
    '21/2': 20.0,
    '23/4': 22.0,
    '3m': 24.0,
    '31/2': 28.0,
}

if __name__ == '__main__':
    df = pd.read_csv('./../outputs/horses.csv', dtype='string')
    jack = horsesClean(df)