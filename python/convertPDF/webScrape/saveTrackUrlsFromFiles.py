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


def saveRaceUrlsFromFiles():
    files = os.listdir('./../yearhtml')
    urls = []
    for file in files:
        dayLinks = getLinks('./../yearhtml/'+file, 'eqbPDFChartPlusIndex.cfm\?tid=')
        urls += generateRaceUrlsFromLinks(dayLinks)
    
    with open('./../excel/raceUrls.csv', 'w') as file:
        for item in urls:
            file.write('%s\n' % item)

saveRaceUrlsFromFiles()