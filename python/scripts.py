import pandas as pd
import json
import psycopg2

from usefulkarisch.fastFunctions import argParseDriver

from convertPDF.webScrape.generateDayLinks import generateDayLinksBetweenDates
from convertPDF.webScrape.htmlMgmt import generateLinksForMissingDays
from convertPDF.webScrape.pdfMgmt import getTrackNamesMissingFromTrackConverter, generateRaceUrlsNotYetSaved, renameAndMovePdfs
from convertPDF.webScrape.pdf2xml import pdf2xml
from convertPDF.webScrape.xml2txt import bulkXml2Txt
from populateDB import generateEntries, populateDB
from dataClean.sql import executeSqlScript
from dataClean.prepForSQL import prepEntriesForSQL

if __name__ == '__main__':
    args = argParseDriver(
        keywords=['scriptName','startDate','endDate', 'schema']
    )
    startDate = pd.to_datetime(args.startDate)
    endDate = pd.to_datetime(args.endDate)

    variables = {
        'renamedPdfFolder': 'C:/Users/jackk/Projects/horseData/charts/pdfs/renamed/',
        'htmlFolder': 'C:/Users/jackk/Projects/horseData/html/',
        'trackConverterAddress': 'C:/Users/jackk/Projects/horseData/excel/tracks_v04.csv',
        'xmlFolder': 'C:/Users/jackk/Projects/horseData/charts/xmls/',
        'txtFolder': 'C:/Users/jackk/Projects/horseData/charts/txts/',
        'entriesJsonAddress': 'C:/Users/jackk/Projects/horseData/outputs/entries.json',
    }
    with open('C:/Users/jackk/Projects/horseData/postgresPassword.txt', 'r') as file:
        variables['postgresPassword'] = file.read()

    match args.scriptName:
        case 'findMissingHtmls':
            generateLinksForMissingDays(
                folderAddress='C:/Users/jackk/Projects/horseData/html/',
                startDate=startDate,
                endDate=endDate,
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/dayLinksTemp.csv'
            )
        case 'saveRaceUrlsFromHtml':
            trackNameAddress = variables['trackConverterAddress']
            trackNameConverterDf = pd.read_csv(trackNameAddress)
            generateRaceUrlsNotYetSaved(
                savedAndRenamedPdfFolder=variables['renamedPdfFolder'],
                trackNameConverterDf=trackNameConverterDf,
                htmlFilesFolder=variables['htmlFolder'],
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/raceUrlsTemp.csv'
            )
        case 'generateDayLinks':
            generateDayLinksBetweenDates(
                startDate=pd.to_datetime(args.startDate),
                endDate=pd.to_datetime(args.endDate),
                csvSaveLocation='C:/Users/jackk/Projects/horseData/excel/dayLinksTemp.csv'
            )
        case 'checkSavedTrackNamesInConverter':
            getTrackNamesMissingFromTrackConverter(
                trackNameConverterAddress=variables['trackConverterAddress'],
                savedAndRenamedResultsPdfsFolder=variables['renamedPdfFolder']
            )
        case 'renameAndMovePdfs':
            renameAndMovePdfs(
                oldDirectory='C:/Users/jackk/Projects/horseData/charts/pdfs/downloads/',
                newDirectory=variables['renamedPdfFolder']
            )
        case 'pdf2xml':
            pdf2xml(
                pdfDir=variables['renamedPdfFolder'],
                xmlDir=variables['xmlFolder']
            )
        case 'xml2txt':
            bulkXml2Txt(
                xmlDir=variables['xmlFolder'],
                txtDir=variables['txtFolder']
            )
        case 'pdf2txt':
            pdf2xml(
                pdfDir=variables['renamedPdfFolder'],
                xmlDir=variables['xmlFolder']
            )
            bulkXml2Txt(
                xmlDir=variables['xmlFolder'],
                txtDir=variables['txtFolder']
            )
        case 'generateAndSaveEntries':
            entries = generateEntries(variables['txtFolder'])
            with open(variables['entriesJsonAddress'], 'w') as file:
                json.dump(entries, file)
        case 'deleteSchemaData':
            if args.schema is None:
                schema = input('Which schema? Enter "test" or "main".\n')
            else:
                schema = args.schema
            if schema == 'test':
                executeSqlScript('C:/Users/jackk/Projects/horseData/sql/deleteDataTest.sql')
            elif schema == 'main':
                response = input('This will delete all data from the "main" schema. Are you sure? [y/n]\n')
                if response == 'y':
                    executeSqlScript('C:/Users/jackk/Projects/horseData/sql/deleteDataMain.sql')
        case 'populateSchema':
            if args.schema is None:
                schema = input('Which schema? Enter "test" or "main".\n')
            conn = psycopg2.connect(
                host = "localhost",
                database = "horses",
                user = "karisch",
                password = variables['postgresPassword'],
                port = 5432
            )
            with open(variables['entriesJsonAddress'], 'r') as file:
                entries = prepEntriesForSQL(json.loads(file.read()))
            populateDB(
                dbConnection=variables['sqlConnection'],
                entries=entries,
                schema=schema
            )