import pytest
import tempo
from tempo import tempoapp


class AppTest(tempoapp.TempoApp):
    kv_file = 'tempo/tempo.kv'

    def on_stop(self):
        return True

    def build(self):
        # tempoapp.Clock.schedule_once(lambda dt: self.stop(), 1.5)
        root = tempoapp.RootWidget()
        return root


@pytest.fixture(scope='module')
def app_launch():
    app = AppTest()
    app.run()
    return app


def test_load_tasks(monkeypatch):
    monkeypatch.setattr(tempoapp, 'DATAFILE', 'tempo/tests/fixtures/data.json')
    r = app.root
    app.stop()
    f = r.load_tasks()
    assert 0
