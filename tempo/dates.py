# import datetime
from datetime import date

HOURSPERDAY = 6

def convert_date(d=date.today()):
    return d.strftime("%d.%m.%Y")


def find_deltatime(starttime: date, endtime: date):
    '''Returns difference in hours between two date objects.'''
    delta = endtime - starttime
    delta = delta.total_seconds()//3600//HOURSPERDAY
    return delta
