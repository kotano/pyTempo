import pytest
import tempo
from tempo import tempoapp
from tempo.tempoapp import RootWidget


class AppTest(tempoapp.TempoApp):
    kv_file = 'tempo/tempo.kv'

    def on_stop(self):
        return True

    def build(self):
        # tempoapp.Clock.schedule_once(lambda dt: self.stop(), 1.5)
        root = tempoapp.RootWidget()
        return root


class Mock(dict):
    pass


# @pytest.fixture
# def app_launch():
#     app = AppTest()
#     app.run()
#     return app


# @pytest.mark.skip
# def test_load_tasks(monkeypatch):
#     monkeypatch.setattr(tempoapp, 'DATAFILE', 'tempo/tests/fixtures/data.json')
#     r = app.root
#     app.stop()
#     f = r.load_tasks()
#     assert 0


def test_find_delta():
    startdate = Mock()
    enddate = Mock()
    startdate.text = '22.06.2020'
    enddate.text = '23.06.2020'
    f = RootWidget().find_delta
    assert f(startdate, enddate) == 6
