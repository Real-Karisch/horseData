from bs4 import BeautifulSoup
import re
import os
import pandas as pd

def getLinks(html, patternStr):
    with open(html) as file:
        raw = file.read()
    soup = BeautifulSoup(raw, features='lxml')

    link = []
    pattern = re.compile(patternStr)
    for i in soup.find_all('a'):
        for key in i.attrs.keys():
            if key == 'href':
                jack = i.get('href')
                if pattern.match(jack) is not None:
                    link.append(jack)
    return link

def generateRaceUrlsFromLinks(dayList):
    urls = []
    for raw in dayList:
        dateIndex = re.search('[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', raw).span()
        trackIndex = list(re.search('tid=...', raw).span())
        trackIndex[0] += 4
        if raw[trackIndex[1] - 1] == "&":
            trackIndex[1] -= 1
        countryIndex = list(re.search('ctry=...', raw).span())
        countryIndex[0] += 5
        if raw[countryIndex[1] - 1] == " ":
            countryIndex[1] -= 1
        

        first = 'https://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID='
        second = '&CTRY='
        third = '&DT='
        fourth = '&DAY=D&STYLE=EQB'
        urls.append(first + raw[trackIndex[0]:trackIndex[1]] + second + raw[countryIndex[0]:countryIndex[1]] + third + raw[dateIndex[0]:dateIndex[1]] + fourth)
    return urls

def generateRaceUrlsFromFiles(filesAddress, csvSaveLocation=None):
    files = os.listdir(filesAddress)
    raceInfo = {
        'track': [],
        'date': [],
        'url': []
    }
    for file in files:
        dayLinks = getLinks(filesAddress+file, r'eqbPDFChartPlusIndex.cfm\?tid=')
        trackUrls = generateRaceUrlsFromLinks(dayLinks)

        for trackUrl in trackUrls:
            search = re.search(r"P=P\&TID=([A-Z]+)\&CTRY=[A-Z]+\&DT=(\d\d/\d\d/\d\d\d\d)", trackUrl)
            track = search.group(1)
            dateStr = search.group(2)
            date = pd.to_datetime(dateStr)
            raceInfo['track'].append(track)
            raceInfo['date'].append(date.strftime('%m/%d/%Y'))
            raceInfo['url'].append(trackUrl)
    
    raceInfoDf = pd.DataFrame(raceInfo)

    if csvSaveLocation is not None:
        raceInfoDf.to_csv(csvSaveLocation, index=False)
    else:
        return raceInfoDf