import os
from os import path
from unittest.mock import Mock

import pytest

from tempo import tempoapp
from tempo import widgets
from tempo.tempoapp import RootWidget, TempoApp


CURRENT_DIR = path.join(path.dirname(__file__))


class AppTest(TempoApp):
    kv_file = 'tempo/tempo.kv'

    def on_stop(self):
        return True

    def schedule_stop(self, sec):
        tempoapp.Clock.schedule_once(lambda dt: self.stop(), sec)

    def build(self):
        root = tempoapp.RootWidget()
        return root


# class RootTest(RootWidget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.APP = AppTest
#         self.APP.worktime = 6


TASKVALUES = {
    'active': True, 'taskname': 'Test',
    'priority': '!Low',
    'startdate': ['22', '06', '2020'],
    'deadline': ['23', '06', '2020'],
    'duration': 4, 'progress': 5,
    'notes': 'Some test note', 'subtasks': []
}


def make_task(name=''):
    v = TASKVALUES
    t = widgets.Task()
    t._active = v['active']
    t._taskname = v['taskname'] if not name else name
    t._priority = v['priority']
    t._startdate = '.'.join(v['startdate'])
    t._deadline = '.'.join(v['deadline'])
    t._duration = v['duration']
    t._progress = v['progress']
    t._notes = v['notes']
    t.subtaskholder = Mock()
    t.subtaskholder.children = v['subtasks']
    return t


@pytest.fixture
def provide_root():
    R = RootWidget()
    R.APP = AppTest
    R.APP.worktime = 6
    taskholder = widgets.Widget(id='taskholder')
    R.taskholder = taskholder
    R.add_widget(taskholder)
    # R.taskholder.children = []
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


def test_task_save_data():
    expected = TASKVALUES
    r = make_task()
    assert r.save_data() == expected


def test_save_tasks(monkeypatch, provide_root):
    r = provide_root
    expected_file = path.join(CURRENT_DIR, 'fixtures', 'tasks.json')
    test_file = path.join(CURRENT_DIR, 'tasks.json')
    monkeypatch.setattr(tempoapp, 'TASKFILE', test_file)
    r.taskholder.children.append(make_task())
    r.save_tasks()
    f1 = open(test_file)
    f2 = open(expected_file)
    assert f1.read() == f2.read()
    f1.close()
    f2.close()
    os.remove(test_file)


# def test_load_tasks(monkeypatch, provide_root):
    # NOTE: Depends much on graphic interface so hard to test.

    # r = provide_root
    # expected_file = path.join(CURRENT_DIR, 'fixtures', 'tasks.json')
    # test_file = path.join(CURRENT_DIR, 'tasks.json')
    # monkeypatch.setattr(tempoapp, 'TASKFILE', expected_file)
    # monkeypatch.setattr(r, 'taskholder', [])
    # t = r.taskholder
    # monkeypatch.setattr(t, 'add_widget', lambda x: [].append(x))
    # f = r.load_tasks()
    # assert 0
