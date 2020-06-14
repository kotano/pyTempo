import pytest

import tempo
from tempo import tempoapp
from tempo import widgets
from tempo.tempoapp import RootWidget, TempoApp


class AppTest(TempoApp):
    kv_file = 'tempo/tempo.kv'

    def on_stop(self):
        return True

    def schedule_stop(self, sec):
        tempoapp.Clock.schedule_once(lambda dt: self.stop(), sec)

    def build(self):
        root = tempoapp.RootWidget()
        return root


class RootTest(RootWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.APP = AppTest
        self.APP.worktime = 6




class Mock(object):
    pass

# @pytest.fixture
# def provide_task():
#     t = widgets.Task
#     t.checkbox = Mock()
#     t.checkbox.active = True
#     t.taskname = Mock()
#     t.taskname.text = 'Test'
#     t.priority = Mock()
#     t.priority.text = '!Low'
#     t.startdate = Mock()
#     t.startdate.active = True

@pytest.fixture
def provide_root():
    R = RootWidget()
    R.APP = AppTest
    R.APP.worktime = 6
    return R


def test_find_delta(provide_root):
    # RootWidget depends on running app instance
    R = provide_root
    startdate = Mock()
    enddate = Mock()
    startdate.text = '22.06.2020'
    enddate.text = '23.06.2020'
    f = R.get_worktime(startdate, enddate)
    assert f == 6

    startdate.text = '21.06.2020'
    enddate.text = '23.06.2020'
    f = R.get_worktime(startdate, enddate)
    assert f == 12


def test_story_save_data():
    expected = {
        'storytext': 'Test', 'postnum': 1,
        'creation': [2020, 6, 14], 'completed_tasks': []}
    s = widgets.Story()
    s._text = 'Test'
    s._tasks = []
    s.postnum = 1
    s.creation = [2020, 6, 14]
    r = s.save_data()
    assert r == expected


# def test_save_tasks():
    # def test_load_tasks(monkeypatch):
    #     monkeypatch.setattr(tempoapp, 'DATAFILE', 'tests/fixtures/data.json')
    #     r = app.root
    #     f = r.load_tasks()
    #     assert 0
