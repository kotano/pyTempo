import datetime
import time
from appsettings import HOURSPERDAY
from builtins import isinstance
from datetime import date, timedelta


def convert_date(d=date.today()):
    if isinstance(d, list):
        return
    return d.strftime("%d.%m.%Y")


def find_time(starttime, deadline):
    delta = deadline - starttime
    delta = delta.total_seconds()//3600//HOURSPERDAY
    return delta
    


if __name__ == "__main__":
    pass
