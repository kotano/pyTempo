import datetime
import time
from tempo import dates


def test_find_deltatime():
    date1 = datetime.date(2020, 6, 22)
    date2 = datetime.date(2020, 6, 23)
    assert 24 == dates.find_deltatime(date1, date2)


def test_find_worktime():
    # If we have one day, so then we have only HOURSPERDAY hours value
    assert dates.HOURSPERDAY == dates.find_worktime(24)
