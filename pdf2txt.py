import os
import re

def pdf2txt(pdfDir, txtDir):
    if pdfDir[-1] != '/':
        pdfDir += '/'
    if txtDir[-1] != '/':
        txtDir += '/'
    files = os.listdir(dir)
    print(len(files))
    for file in files:
        address = "'" + pdfDir + file + "'"
        output = "'" + txtDir + re.sub('pdf', 'txt', file) + "'"
        command = 'gs -sDEVICE=txtwrite -o '+ output + ' ' + address
        os.system(command)