import pytest
import tempo
from tempo import tempoapp
from tempo.tempoapp import RootWidget


class AppTest(tempoapp.TempoApp):
    kv_file = 'tempo/tempo.kv'

    def on_stop(self):
        return True

    def sched_stop(self, sec):
        tempoapp.Clock.schedule_once(lambda dt: self.stop(), sec)

    def build(self):
        root = tempoapp.RootWidget()
        return root


class Mock(dict):
    pass


# def test_load_tasks(monkeypatch):
#     monkeypatch.setattr(tempoapp, 'DATAFILE', 'tests/fixtures/data.json')
#     r = app.root
#     f = r.load_tasks()
#     assert 0


def test_find_delta():
    startdate = Mock()
    enddate = Mock()
    startdate.text = '22.06.2020'
    enddate.text = '23.06.2020'
    f = RootWidget().get_worktime
    assert f(startdate, enddate) == 6
