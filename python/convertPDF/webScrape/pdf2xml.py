import os
import re

def pdf2xml(pdfDir, xmlDir):
    if pdfDir[-1] != '/':
        pdfDir += '/'
    if xmlDir[-1] != '/':
        xmlDir += '/'
    files = os.listdir(pdfDir)
    print('Converting ', str(len(files)), 'files')
    for file in files:
        if re.search(r'\.pdf', file) is None:
            continue
        address = "'" + pdfDir + file + "'"
        output = "'" + xmlDir + re.sub('pdf', 'txt', file) + "'"
        command = 'gs -sDEVICE=txtwrite -dTextFormat=0 -o '+ output + ' ' + address
        os.system(command)