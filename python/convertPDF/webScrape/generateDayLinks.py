import pandas as pd
from datetime import timedelta

def generateDayLink(date):
    link = f'https://www.equibase.com/premium/eqpVchartBuy.cfm?mo={date.month}&da={date.day}&yr={date.year}&trackco=ALL;ALL&cl=Y'
    return link

def generateDayLinksBetweenDates(startDate, endDate, csvSaveLocation=None):
    activeDate = startDate
    datesAndLinks = {
        'date': [],
        'link': []
    }
    while activeDate <= endDate:
        datesAndLinks['date'].append(activeDate)
        datesAndLinks['link'].append(
            generateDayLink(activeDate)
        )
        activeDate = activeDate + timedelta(days=1)
    if csvSaveLocation is not None:
        pd.DataFrame(datesAndLinks).to_csv(csvSaveLocation, index=False)
    else:
        return datesAndLinks

def generateDayLinksOnDates(dates):
    links = []
    for date in dates:
        links.append(
            generateDayLink(date)
        )
    return links