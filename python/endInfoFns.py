import re
import pandas as pd

def parseEndInfo(endLines):

    cnt = 0
    for line in endLines:
        if re.match(r'^ Trainers:', line) is not None:
            trainerInd = cnt
        elif re.match(r'^ Owners:', line) is not None:
            trainerInd.append(cnt)
            ownerInd = cnt
        elif re.match(r'^ Footnotes$', line) is not None:
            ownerInd.append(cnt)
    
    trainerLine = ''.join([line[:-1] for line in endLines[trainerInd[0]: trainerInd[1]]])
    ownerLine = ''.join([line[:-1] for line in endLines[ownerInd[0]: ownerInd[1]]])

    trainers = parseTrainerLine(trainerLine)
    owners = parseOwnerLine(ownerLine)

    