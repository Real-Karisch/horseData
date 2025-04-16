import os
import re
import subprocess

def pdf2xml(pdfDir, xmlDir):
    if pdfDir[-1] != '/':
        pdfDir += '/'
    if xmlDir[-1] != '/':
        xmlDir += '/'
    files = os.listdir(pdfDir)
    alreadyRun = os.listdir(xmlDir)

    print('Converting ', str(len(files)), 'files')
    for file in files:
        if re.search(r'\.pdf', file) is None:
            print(f"Skipping {file} because it is not a pdf.")
            continue
        if re.sub('pdf', 'txt', file) in alreadyRun:
            #print(f"Skipping {file} because it has already been run.")
            continue
        address = f"'{pdfDir}{file}'"
        output = f"'{xmlDir}{re.sub('pdf', 'txt', file)}'"
        command = 'gswin64c -sDEVICE=txtwrite -dTextFormat=0 -o '+ output + ' ' + address
        subprocess.call(f"C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe {command}")

if __name__ == '__main__':
    pdf2xml(
        pdfDir='C:/Users/jackk/Projects/horseData/charts/pdfs/renamed/',
        xmlDir='C:/Users/jackk/Projects/horseData/charts/xmls/'
    )