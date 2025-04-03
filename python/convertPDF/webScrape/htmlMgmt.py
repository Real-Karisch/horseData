import os
import re
import pandas as pd
from bs4 import BeautifulSoup

def renameHtml(folderAddress):
    fileNames = os.listdir(folderAddress)
    for fileName in fileNames:
        with open(folderAddress + '/' + fileName) as file:
            raw = file.read()

            soup = BeautifulSoup(raw, 'html.parser')

            date = re.search(r', (.*)', soup.center.text.strip()).group(1)

        os.rename(folderAddress + '/' + fileName, folderAddress + '/' + date + '.html')
            

def generateTrackKey(htmlFileAddress, outputCsvAddress):
    out = {'shortName': [], 'fullName': []}

    with open(htmlFileAddress) as file:
        raw = file.read()
    
    soup = BeautifulSoup(raw, 'html.parser')

    tracksRaw = soup.find_all('div')[88].find_all('option')

    for i in range(1, len(tracksRaw)):
        search = re.search(r'([A-Z0-9]{2,3}) +- (.*)', tracksRaw[i].text)
        shortName = search.group(1).strip()
        fullName = re.sub(r'[^A-Za-z ]', '', search.group(2).strip())

        out['shortName'].append(shortName)
        out['fullName'].append(fullName)

    extras = {
        'shortName': [
            'PMT',
            'UN',
            'EDR',
            'CHA',
        ],
        'fullName': [
            'PINE MTNCALLAWAY GARDEN',
            'EASTERN OREGON LIVESTOCK SHO W',
            'ENERGY DOWNS',
            'CHARLESTON',
        ]
    }

    out['shortName'].extend(extras['shortName'])
    out['fullName'].extend(extras['fullName'])

    outdf = pd.DataFrame(out)
    outdf.to_csv(outputCsvAddress + '/tracks.csv', index=False)