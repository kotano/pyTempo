import json
import os
from collections import OrderedDict
import datetime
import dates

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from task import SUBTASK, TASK
# from KivyCalendar import CalendarWidget, DatePicker

DATAFILE = os.path.join(os.path.dirname(__file__), 'data.json')


class TaskStatus(CheckBox):
    pass

class DateInput(TextInput):
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

    def set_time_on_focus(self, value, starttime, deadline):
        if value:
            print('User focused', instance)
            return '1'
        else:
            print('User defocused', instance)
            return self.set_time(starttime, deadline)


    def load_tasks(self, dt):
        try:
            with open(DATAFILE, 'r') as datafile:
                tasks = json.load(datafile)
                for t in tasks.values():
                    widget = TASK.format(
                        active=t['active'], taskname=t['taskname'],
                        priority=t['priority'],
                        startdate='.'.join(t['startdate']),
                        time=t['time'], progress=t['progress'],
                        deadline='.'.join(t['deadline']), notes=t['notes']
                    )
                    self.taskholder.add_widget(Builder.load_string(widget))
        except (FileNotFoundError):
            print('File does not exist. Creating new one')
    
    def set_time(self, time, val, startdate, deadline):
        if not val:
            try:
                start = dates.convert_date() if startdate.text == '' else  [
                    int(x) for x in startdate.text.split('.')][::-1]
                end = dates.convert_date() if deadline.text == '' else [
                    int(x) for x in deadline.text.split('.')][::-1]
            except ValueError:
                print('You have entered wrong data')
            else:
                res = dates.find_time(start, end)
                time.text = str(res)
                print(start, end)
                
                return res

    def save_tasks(self, *args):
        data = {}
        counter = 1
        for task in self.taskholder.children[::-1]:
            data.update({counter: {
                'active': task.checkbox.active,
                'taskname': task.taskname.text,
                'priority': task.priority.text,
                'startdate': task.startdate.text.split('.'),
                'time': task.time.text,
                'progress': task.progress.text,
                'deadline': task.deadline.text.split('.'),
                'notes': task.notes.text,
            }})
            print(data)
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(DATAFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def add_list_item(self):
        widget = TASK.format(
            active=False, taskname='', priority='-',
            startdate=dates.convert_date(), time='', progress='0', deadline='',
            notes=''
            )
        # widget = TASK
        self.taskholder.add_widget(Builder.load_string(widget))
        self.taskholder.children[0].popup.open()




class TempoApp(App):
    def build(self):
        app = RootWidget()
        try:
            Clock.schedule_once(app.load_tasks)
        except Exception as e:
            print(e)

        Clock.schedule_interval(app.save_tasks, 15)
        return app


if __name__ == '__main__':
    TempoApp().run()
