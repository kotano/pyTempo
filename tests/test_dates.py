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


def test_date_to_string():
    d = datetime.date(2020, 6, 22)
    assert '22.06.2020' == dates.date_to_string(d)


def test_convert_to_date():
    s = '22.06.2020'
    assert datetime.date(2020, 6, 22) == dates.convert_to_date(s)
