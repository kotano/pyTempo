import sys
import time
import datetime
from datetime import date

from plyer import notification, vibrator
from plyer.utils import platform


# from tempo.config import POMODORO_DURATION, POMODORO_REST, WORKTIME

cur_month = date.today().month
cur_year = date.today().year
cur_date = date.today()


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


def find_worktime(hours):
    '''Find available work time per day. Return int'''
    days = hours // 24
    work_hours = days * WORKTIME
    return work_hours


def notify(title, message, mode='normal'):
    """Send system notification.

    Args:
        title (str): Notification title
        message (str): Message main text
        mode (str, optional): Notification mode
            choose from ['normal', 'fancy']. Defaults to 'normal'.
    """
    icon = None
    if platform == 'ios':
        return
    if mode == 'fancy':
        if platform == 'win':
            pass
        else:
            icon = './data/icons/logo.png'
    notification.notify(title=title, message=message, app_icon=icon)


def vibrate(time, pattern=[0, 1]):
    pass


# class NotificationDemo(BoxLayout):

#     def do_notify(self, mode='normal'):
#         kwargs = {'title': title, 'message': message, 'ticker': ticker}

#         if mode == 'fancy':
#             kwargs['app_name'] = "Plyer Notification Example"
#             if platform == "win":
#                 kwargs['app_icon'] = join(dirname(realpath(__file__)),
#                                           'plyer-icon.ico')
#                 kwargs['timeout'] = 4
#             else:
#                 kwargs['app_icon'] = join(dirname(realpath(__file__)),
#                                           'plyer-icon.png')
#         elif mode == 'toast':
#             kwargs['toast'] = True
#         notification.notify(**kwargs)
