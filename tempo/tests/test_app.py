import datetime

# from tempo import tempoapp


# class TestApp(tempoapp.TempoApp):
#     def build(self):
#         tempoapp.Clock.schedule_once(self.stop, 3)
#         super().build()


def test_find_deltatime():
    date1 = datetime.date(2020, 6, 22)
    date2 = datetime.date(2020, 6, 23)
    delta = date2 - date1
    print(delta)
    # dates.find_deltatime(dates.date.today)
