import json
import os
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    ListProperty, NumericProperty, ObjectProperty, StringProperty)

from kivy.graphics.instructions import Canvas
from kivy.lang.builder import Builder
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
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from kivy.uix.bubble import Bubble

DATAFILE = os.path.join(os.path.dirname(__file__), 'data.json')


TASKDATA = ('''
Task:
    id: task
    taskname: taskname.__self__
    priority: priority.__self__
    time: time.__self__
    deadline: deadline.__self__
    checkbox: checkbox.__self__
    
    popup: popup.__self__
    notes: notes.__self__
    

    # on_parent: app.root.save_tasks(self.taskname.text, self.priority.text, self.time.text, self.deadline.text)
    
    # checkbox
    CheckBox:
        id: checkbox
        active: {active}
        size_hint: None, 1
        width: 20
        pos: root.center
    
# TASKNAME # POPUP
    BoxLayout:
        size_hint_x: 2
        id: bl

        Popup:
            id: popup
            title: "Edit task"
            # background_color: 1, 1, 1, 1
            on_parent:
                if self.parent == bl: self.parent.remove_widget(self)
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                background_color: 1, 1, 1, 1
                orientation: 'vertical'

                BoxLayout:
                    size_hint: 1, None
                    height: 50
                    spacing: 40, 40

                    PrioritySpinner:
                        text: priority.text
                        size_hint: 0.1, 1

                    TextInput:
                        id: taskname
                        text: '{taskname}'
                        write_tab: False
                        focus: True
                        hint_text: 'Enter task name'
                        multiline: False
                        size_hint: 0.8, 1


                BoxLayout:
                    padding: 10, 10
                    size_hint_y: None
                    height: 50

                    TextInput:
                        size_hint_x: 0.25
                        text: 'xx/xx/xxxx'
                    Button:
                        size_hint_x: 0.5
                        text: '23 HOURS OF 30'
                    TextInput:
                        size_hint_x: 0.25
                        text: 'xx/xx/xxxx'
                        
                
                
                TextInput:
                    id: notes
                    text: '{notes}'
                    hint_text: 'Notes...'
                    size_hint: 1, 1
                    height: 100
                BoxLayout:
                    size_hint_y: None
                    height: 50
                    
                    Button:
                        text: 'Save'
                        on_release: 
                            popup.dismiss();
                            app.root.save_tasks();
                    Button:
                        text: 'Delete'
                        size_hint_x: None
                        width: 50
                        background_color: 1, 0, 0, 1
                        on_release:
                            app.root.taskholder.remove_widget(task);
                            popup.dismiss();
                            app.root.save_tasks();

        Button:
            background_normal: ''
            color: 0, 0, 0, 1
            text: taskname.text
            on_release: root.popup.open()

    # # taskname
    # TextInput:
    #     id: taskname
    #     text: '{taskname}'
    #     write_tab: False
    #     focus: True
    #     hint_text: 'My new task!'
    #     multiline: False
    #     size_hint_x: 2
    
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


class TaskStatus(CheckBox):
    pass


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
        try:
            with open(DATAFILE, 'r') as datafile:
                tasks = json.load(datafile)
                # tasks = OrderedDict(sorted(tasks.items(), key= lambda t: t[0]))
                # tasks = dict(sorted(tasks.items(), key= lambda t: t[0]))
                for t in tasks.values():
                    widget = TASKDATA.format(
                        active=t['active'], taskname=t['taskname'], priority=t['priority'], time=t['time'], deadline=t['deadline'], notes=t['notes']
                    )
                    self.taskholder.add_widget(Builder.load_string(widget))
        except FileNotFoundError:
            print('File does not exist. Creating new one')

    def save_tasks(self, *args):
        data = {}
        counter = 1
        for task in self.taskholder.children[::-1]:
            data.update({counter: {
                'active': task.checkbox.active,
                'taskname': task.taskname.text,
                'priority': task.priority.text,
                'time': task.time.text,
                'deadline': task.deadline.text,
                'notes': task.notes.text,
            }})
            print(data)
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(DATAFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def add_list_item(self):
        widget = TASKDATA.format(
            active=False, taskname='', priority='-', time='', deadline='', notes='')
        self.taskholder.add_widget(Builder.load_string(widget))
        self.taskholder.children[0].popup.open()


class TempoApp(App):
    def build(self):
        app = RootWidget()
        try:
            Clock.schedule_once(app.load_tasks)
        except Exception as e:
            print(e)

        Clock.schedule_interval(app.save_tasks, 5)
        return app


if __name__ == '__main__':
    TempoApp().run()
