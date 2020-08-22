import re
import pandas as pd

def parseEndInfo(endLines):

    cnt = 0
    for line in endLines:
        if re.match(r'^ Trainers:', line) is not None:
            trainerInd = [cnt]
        elif re.match(r'^ Owners:', line) is not None:
            trainerInd.append(cnt)
            ownerInd = [cnt]
        elif re.match(r'^ Footnotes$', line) is not None:
            ownerInd.append(cnt)
        cnt += 1
    
    trainerLine = ''.join([line[:-1] for line in endLines[trainerInd[0]: trainerInd[1]]]) + ';'
    ownerLine = ''.join([line[:-1] for line in endLines[ownerInd[0]: ownerInd[1]]])

    trainersDF = parseTrainerLine(trainerLine)
    ownersDF = parseOwnerLine(ownerLine)

    fullDF = pd.merge(trainersDF, ownersDF, how = 'outer', on='program')

    return fullDF


def parseTrainerLine(line):
    endDF = pd.DataFrame(columns=['program','trainer'])

    fullSearch = re.search(r'( \d?\d - [^;]+;)+', line)
    split = fullSearch.group(0).split(';')[:-1]

    for item in split:
        shortSearch = re.search(r'(\d?\d) - (.+)$', item)

        endDF = pd.concat([endDF, (pd.DataFrame(data=[[shortSearch.group(1),shortSearch.group(2)]],columns=['program','trainer']))])

    return endDF

def parseOwnerLine(line):
    endDF = pd.DataFrame(columns=['program','owner'])

    fullSearch = re.search(r'( \d?\d - ?[^;]+;)+', line)
    split = fullSearch.group(0).split(';')[:-1]

    for item in split:
        shortSearch = re.search(r'^ (\d?\d) - ?(.+)$', item)

        endDF = pd.concat([endDF, (pd.DataFrame(data=[[shortSearch.group(1),shortSearch.group(2)]],columns=['program','owner']))])

    return endDF