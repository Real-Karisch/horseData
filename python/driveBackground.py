from convertPDF.webScrape.pdf2xml import *
from convertPDF.webScrape.xml2txt import *

pdfDir = 'C:/Users/jackk/Projects/horseData/charts/pdfs/renamed/'
xmlDir = 'C:/Users/jackk/Projects/horseData/charts/xmls/'
txtDir = 'C:/Users/jackk/Projects/horseData/charts/txts/'

pdf2xml(
    pdfDir=pdfDir,
    xmlDir=xmlDir
)
bulkXml2Txt(
    xmlDir=xmlDir,
    txtDir=txtDir
)