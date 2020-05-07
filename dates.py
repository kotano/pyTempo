# import datetime
from datetime import date

HOURSPERDAY = 6

def date_to_string(d=date.today()):
    '''Return dd:mm:yy format string from date object.'''
    return d.strftime("%d.%m.%Y")

def convert_to_date(arg):
    '''Convert list or str in dd:mm:yy: format and return date object.'''
    if isinstance(arg, str):
        res = [int(x) for x in arg.split('.')][::-1]
        return date(*res)
    return date(*arg)

def find_deltatime(starttime: date, endtime: date):
    '''Return difference in hours between two dates.'''
    delta = endtime - starttime
    delta = delta.total_seconds()//3600//HOURSPERDAY
    return delta
