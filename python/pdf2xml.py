import os
import re

def pdf2xml(pdfDir, xmlDir):
    if pdfDir[-1] != '/':
        pdfDir += '/'
    if xmlDir[-1] != '/':
        xmlDir += '/'
    files = os.listdir(pdfDir)
    print('Converting ' + len(files) + 'files')
    for file in files:
        address = "'" + pdfDir + file + "'"
        output = "'" + xmlDir + re.sub('pdf', 'txt', file) + "'"
        command = 'gs -sDEVICE=txtwrite -dTextFormat=0 -o '+ output + ' ' + address
        os.system(command)