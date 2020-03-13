import json
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.instructions import Canvas
from kivy.lang.builder import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

DATAFILE = os.path.join(os.path.dirname(__file__), 'data.json')


TASKDATA = ('''
Task:
    id: task
    # taskid: task.__self__
    taskname: taskname.__self__
    priority: priority.__self__
    time: time.__self__
    deadline: deadline.__self__

    # on_parent: app.root.save_tasks(self.taskname.text, self.priority.text, self.time.text, self.deadline.text)
    
    # checkbox
    CheckBox:
        size_hint: 0.2, 0.2
        pos: root.center
    
    # taskname
    TextInput:
        text: '{taskname}'
        id: taskname
        focus: True
        hint_text: 'My new task!'
        multiline: False
        size_hint_x: 2
    
    PrioritySpinner:
        id: priority
        text: '{priority}'
    
    ListLabel:
        id: time
        text: '{time}'
    
    ListLabel:
        id: deadline
        text: '{deadline}' 
''')

class Task(BoxLayout):
    pass


class PriorityDropdown(BoxLayout):
    pass

class PrioritySpinner(Spinner):
    pass


class RootWidget(BoxLayout):
    taskholder = ObjectProperty()
    task_ids = ListProperty([])
    idscounter = NumericProperty(1)

    def load_tasks(self, dt):
        with open(DATAFILE, 'r') as datafile:
            tasks = json.load(datafile)
            for task in tasks:
                self.add_list_item()

    def save_tasks(self, *args):
        data = {}
        counter = 1
        for task in self.taskholder.children:
            data.update({counter:{
                'taskname': task.taskname.text,
                'priority': task.priority.text,
                'time': task.time.text,
                'deadline': task.deadline.text,
            }})
            print(data)
            counter += 1
        with open(DATAFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def add_list_item(self, *args):
        task = Task()
        # taskdata = TASKDATA.format()
        if not args:
            self.taskholder.add_widget(Builder.load_string(TASKDATA.format(taskname='', priority='-', time='', deadline='')))
            self.idscounter += 1
        else:
            tasks = args[0]
            for t in tasks:
                self.taskholder.add_widget(Builder.load_string(TASKDATA.format(taskname=t['taskname'], priority=t['priority'], time=t['time'], deadline=t['deadline'])))
                self.idscounter += 1
        # self.taskholder.add_widget(task)


class TempoApp(App):
    def build(self):
        app = RootWidget()
        Clock.schedule_once(app.load_tasks)
        Clock.schedule_interval(app.save_tasks, 5)
        return app


if __name__ == '__main__':
    TempoApp().run()
