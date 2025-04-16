import pandas as pd

from usefulkarisch.fastFunctions import argParseDriver

from convertPDF.webScrape.generateDayLinks import generateDayLinksBetweenDates
from convertPDF.webScrape.htmlMgmt import generateLinksForMissingDays
from convertPDF.webScrape.saveTrackUrlsFromFiles import saveRaceUrlsFromFiles

if __name__ == '__main__':
    args = argParseDriver(
        keywords=['scriptName','startDate','endDate']
    )
    startDate = pd.to_datetime(args.startDate)
    endDate = pd.to_datetime(args.endDate)
    match args.scriptName:
        case 'findMissingHtmls':
            generateLinksForMissingDays(
                folderAddress='C:/Users/jackk/Projects/horseData/html/',
                startDate=startDate,
                endDate=endDate,
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/dayLinksTemp.csv'
            )
        case 'saveRaceUrlsFromHtml':
            saveRaceUrlsFromFiles(
                filesAddress='C:/Users/jackk/Projects/horseData/html/',
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/raceUrlsTemp.csv'
            )
        case 'generateDayLinks':
            generateDayLinksBetweenDates(
                startDate=pd.to_datetime(args.startDate),
                endDate=pd.to_datetime(args.endDate),
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/dayLinksTemp.csv'
            )