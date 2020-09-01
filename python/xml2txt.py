from bs4 import BeautifulSoup
import re
import os

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
            size = int(span.get('size')[0])
            for char in charList:
                bbox = char.get('bbox')
                c = char.get('c')
                bboxSearch = re.search('(\d+) (\d+) (\d+) \d+', bbox)
                if bboxSearch is None:
                    print('Error - no match')
                    print('Page =', i)
                    print('bbox =', bbox)
                    print('Character =', c)
                    input('Press enter to continue')
                    continue
                    
                beginCol = int(bboxSearch.group(1))
                pdfRow = int(bboxSearch.group(2))
                endCol = int(bboxSearch.group(3))
                txtRow = lines[i][pdfRow]

                if beginCol == lastColInd[txtRow] or (size == 6 and (beginCol - lastColInd[txtRow]) <= 2):
                    pageTxt[txtRow] += c
                else:
                    pageTxt[txtRow] += ' ' + c

                lastColInd[txtRow] = endCol
        
        txt += pageTxt

    txt = [x for x in txt if x != '']

    with open(outputFile, 'w') as file:
        for line in txt:
            file.write('%s\n' % line)

def bulkXml2Txt(xmlDir, txtDir):
    if txtDir[-1] != '/':
        txtDir += '/'
    if xmlDir[-1] != '/':
        xmlDir += '/'
    filenames = os.listdir(xmlDir)
    extantFiles = os.listdir(txtDir)
    print('Converting ' + str(len(filenames)) + ' files')
    cnt = 0
    for filename in filenames:
        cnt += 1
        if filename in extantFiles:
            continue
        print(filename) #delete this once working
        with open(xmlDir + filename) as file:
            rawXml = file.read()
            soup = BeautifulSoup(rawXml, 'html.parser')
    
        createTxtFromXml(soup, txtDir + filename)

        if cnt % 20 == 0:
            perc = cnt / len(filenames) * 100
            print('Progress: %.1f%%' % perc)