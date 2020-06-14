import sys
import time
import datetime
from datetime import date

from plyer import notification, vibrator
from plyer.utils import platform


# TODO: Make a function
cur_month = date.today().month
cur_year = date.today().year
cur_date = date.today()


def print_log(func):
    """Decorator function to track functions execution."""

    def wrapper(*args, **kwargs):
        n = func.__name__
        print('{} has started with arguments:\n{}\n{}'.format(
            n, args, kwargs))
        res = func(*args, **kwargs)
        print('{} has finished and returned: {}'.format(
            n, res))
        return res

    return wrapper


def date_to_string(d=date.today()):
    '''Return dd:mm:yy format string from date object.'''
    return d.strftime("%d.%m.%Y")


def date_to_list(d=date.today()):
    '''Return dd:mm:yy format list from date object.'''
    return [d.year, d.month, d.day]


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


def find_worktime(hours, worktime=6):
    '''Find available work time per day. Return int'''
    days = hours // 24
    work_hours = days * worktime
    return work_hours


def notify(title, message, mode='normal'):
    """Send system notification.

    Args:
        title (str): Notification title
        message (str): Message main text
        mode (str, optional): Notification mode
            choose from ['normal', 'fancy', 'toast']. Defaults to 'normal'.
    """
    kwargs = {
        'app_name': 'Tempo',
        'app_icon': './data/icons/logo.png',
        'title': title, 'message': message,
        # Ticker is a text to display on status bar when notification arrives.
        'ticker': None, 'timeout': 10,
        # Toast is a simple android message instead of full notification.
        'toast': False
    }
    # Not implemented yet for ios.
    if platform == 'ios':
        return
    elif platform == 'win':
        # TODO: Make app logo.ico file
        kwargs['app_icon'] = None
        kwargs['timeout'] = 4
    elif platform == 'android' and mode == 'toast':
        kwargs['toast': True]
    notification.notify(**kwargs)


def vibrate(time, pattern=[0, 1]):
    pass
