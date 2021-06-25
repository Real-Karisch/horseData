import os
import re
from bs4 import BeautifulSoup

def renameHtml(folderAddress):
    fileNames = os.listdir(folderAddress)
    for fileName in fileNames:
        with open(folderAddress + '/' + fileName) as file:
            raw = file.read()

            soup = BeautifulSoup(raw, 'html.parser')

            date = re.search(r', (.*)', soup.center.text.strip()).group(1)

            os.rename(folderAddress + '/' + fileName, folderAddress + '/' + date + '.html')