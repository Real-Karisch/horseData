from convertPDF.infoFns.genInfoFns import parseDistanceSurface
from convertPDF.driver import parseFullDay

with open('./../charts/txts/eqbPDFChartPlus - 2021-06-25T172752.327.txt') as file:
    full = file.read()

jack = parseFullDay(full)