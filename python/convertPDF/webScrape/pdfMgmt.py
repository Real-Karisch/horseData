import os
import re
import shutil
import pandas as pd
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

if __name__ == '__main__':
    from saveTrackUrlsFromFiles import generateRaceUrlsFromFiles
else:
    from .saveTrackUrlsFromFiles import generateRaceUrlsFromFiles

def getTrackNameAndDateFromPdfFileName(pdfFileName):
    search = re.search(r"^([A-Z]+)_(.+)\.pdf$", pdfFileName)
    trackName = search.group(1)
    date = pd.to_datetime(search.group(2))
    return {
        'trackName': trackName,
        'date': date.strftime('%m/%d/%Y')
    }

def getSavedTrackNamesAndDates(pdfFilesLocation):
    allFiles = os.listdir(pdfFilesLocation)
    tracksAndDates = {
        'trackName': [],
        'date': []
    }
    for file in allFiles:
        pdfFileNameInfo  = getTrackNameAndDateFromPdfFileName(file)
        tracksAndDates['trackName'].append(pdfFileNameInfo['trackName'])
        tracksAndDates['date'].append(pdfFileNameInfo['date'])
    
    tracksAndDatesDf = pd.DataFrame(tracksAndDates)
    return tracksAndDatesDf

def renameAndMovePdfs(
    oldDirectory,
    newDirectory
):
    alreadyConvertedFiles = os.listdir(newDirectory)
    pdfNames = [x for x in os.listdir(oldDirectory) if re.search(r'\.pdf$',x)]

    dates = []
    tracks = []
    errors = []
    for filename in pdfNames:
        try:
            reader = PdfReader(f"{oldDirectory}/{filename}")
        except PdfReadError:
            print(f'PDF read error in {filename}.')
            errors.append(filename)
            continue
        firstLine = reader.pages[0].extract_text().split('\n')[0]
        trackAndDateSearch = re.search(r"^(.+)- ([A-Za-z]+ \d+, \d+) *-", firstLine)
        track = re.sub(r'[^A-Z]', '', trackAndDateSearch.group(1))
        dateStr = trackAndDateSearch.group(2)
        date = pd.to_datetime(dateStr)
        if track not in tracks:
            tracks.append(track)
        if date not in dates:
            dates.append(date)

        newFileName = f"{track}_{date.strftime('%m.%d.%Y')}.pdf"

        if newFileName not in alreadyConvertedFiles:
            shutil.move(
                src=f"{oldDirectory}/{filename}",
                dst=f"{newDirectory}/{newFileName}"
            )
        else:
            os.remove(f"{oldDirectory}/{filename}")

def generateRaceUrlsNotYetSaved(
    savedAndRenamedPdfFolder,
    trackNameConverterDf,
    htmlFilesFolder,
    csvSaveLocation=None
):
    trackNameAbbreviationToFullStripped = {trackNameConverterDf.loc[i, 'abbreviation']: trackNameConverterDf.loc[i, 'pdfStripSpaces'] for i in trackNameConverterDf.index}

    filesFromHtml = generateRaceUrlsFromFiles(htmlFilesFolder)
    alreadySavedFiles = getSavedTrackNamesAndDates(savedAndRenamedPdfFolder)
    filesFromHtml = (
        filesFromHtml
            .assign(
                fullStrippedWithDate = lambda df: df['track'].apply(
                    lambda x: trackNameAbbreviationToFullStripped[x]
                ) + df['date']
            )
    )
    alreadySavedFiles = (
        alreadySavedFiles
            .assign(
                fullStrippedWithDate = lambda df: df['trackName'] + df['date']
            )
    )
    unsavedUrls = pd.DataFrame(columns=filesFromHtml.columns)
    for i in filesFromHtml.index:
        if filesFromHtml.loc[i, 'fullStrippedWithDate'] not in list(alreadySavedFiles['fullStrippedWithDate']):
            unsavedUrls.loc[unsavedUrls.shape[0]] = filesFromHtml.loc[i]

    unsavedUrls = unsavedUrls.drop(columns=['fullStrippedWithDate'])

    if csvSaveLocation is not None:
        unsavedUrls.to_csv(csvSaveLocation, index=False)
    else:
        return unsavedUrls 
    
def getTrackNamesMissingFromTrackConverter(
    trackNameConverterAddress,
    savedAndRenamedResultsPdfsFolder,
):
    trackNameConverterDf = pd.read_csv(trackNameConverterAddress)
    alreadySavedFiles = getSavedTrackNamesAndDates(savedAndRenamedResultsPdfsFolder)
    missingFromConverter = {
        'track': [],
        'date': []
    }
    for i in alreadySavedFiles.index:
        if alreadySavedFiles.loc[i, 'trackName'] not in list(trackNameConverterDf['pdfStripSpaces']):
            missingFromConverter['track'].append(alreadySavedFiles.loc[i, 'trackName'])
            missingFromConverter['date'].append(alreadySavedFiles.loc[i, 'date'])
    missingFromConverterDf = pd.DataFrame(missingFromConverter)
    print()
    if missingFromConverterDf.empty:
        print(f'All saved tracks present in {trackNameConverterAddress}.')
    else:
        print(f"{trackNameConverterAddress} missing the following tracks:")
        print(f"{','.join(missingFromConverterDf['track'].unique())}")
    print()