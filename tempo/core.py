import datetime
import time
from builtins import isinstance
from datetime import date, timedelta


def convert_date(d=date.today()):
    if isinstance(d, list):
        return
    return d.strftime("%d.%m.%Y")


def find_time():
    pass


if __name__ == "__main__":
    pass
