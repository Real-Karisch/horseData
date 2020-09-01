from bs4 import BeautifulSoup
import re

"""
function to return all the unique rows found in a single race pdf, sorted by page number and line number

input: soupObj, a BeautifulSoup object of the parsed xml of a race pdf
output: a list of dicts, each representing a different page, each mapping a particular line in the pdf to a line in the output txt
"""
def uniqueXmlRows(soupObj):
    pageList = soupObj.find_all('page')

    pages = []
    for i in range(len(pageList)):
        page = pageList[i]
        spanList = page.find_all('span')

        row = []
        for span in spanList:
            bbox = span.get('bbox')
            bboxSearch = re.search('\d+ (\d+) \d+ (\d+)', bbox)
            row.append(int(bboxSearch.group(1)))

        rowUnique = sorted(list(set(row)))
        rowIndex = list(range(len(rowUnique)))

        rowDict = dict(zip(rowUnique,rowIndex))
        pages.append(rowDict)

    return pages

"""
function to generate a txt file from the xml of a pdf of a result chart from equibase
inputs:
    soupObj: a BeautifulSoup object
    outputFile: a string address for the output txt
outputs a txt file in the system at the address provided
"""
def createTxtFromXml(soupObj, outputFile):
    lines = uniqueXmlRows(soupObj)

    pageList = soupObj.find_all('page')
    txt = []

    for i in range(len(pageList)):
        page = pageList[i]

        lastColInd = [0] * len(lines[i])
        pageTxt = [''] * len(lines[i])

        spanList = page.find_all('span')
        for span in spanList:
            charList = span.find_all('char')
            for char in charList:
                bbox = char.get('bbox')
                c = char.get('c')
                bboxSearch = re.search('(\d+) (\d+) (\d+) \d+', bbox)
                beginCol = int(bboxSearch.group(1))
                pdfRow = int(bboxSearch.group(2))
                endCol = int(bboxSearch.group(3))
                txtRow = lines[i][pdfRow]

                if beginCol == lastColInd[txtRow]:
                    pageTxt[txtRow] += c
                else:
                    pageTxt[txtRow] += ' ' + c

                lastColInd[txtRow] = endCol
        
        txt += pageTxt

    txt = [x for x in txt if x != '']

    with open(outputFile, 'w') as file:
        for line in txt:
            file.write('%s\n' % line)