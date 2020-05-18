import sys
import time
from datetime import date

HOURSPERDAY = 6
POMODORO_DURATION = 25
POMODORO_REST = 5


def date_to_string(d=date.today()):
    '''Return dd:mm:yy format string from date object.'''
    return d.strftime("%d.%m.%Y")


def convert_to_date(arg):
    '''Convert list or str in dd:mm:yy: format to date object and return it.'''
    if isinstance(arg, str):
        res = [int(x) for x in arg.split('.')][::-1]
        return date(*res)
    return date(*arg)


def find_deltatime(starttime: date, endtime: date):
    '''Return difference in hours between two dates. '''
    delta = endtime - starttime
    hours = delta.total_seconds()//3600
    return hours

def find_worktime(hours):
    '''Find available work time per day. Return int'''
    days = hours // 24
    work_hours = days * HOURSPERDAY
    return work_hours
