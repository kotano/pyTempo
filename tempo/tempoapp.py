import json
import os
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout

from tempo import dates
from tempo.task import SUBTASK, TASK

# from KivyCalendar import CalendarWidget, DatePicker



DATAFILE = os.path.join(os.path.dirname(__file__), 'data.json')


class Task(BoxLayout):
    pass


class Subtask(Task):
    pass


class RootWidget(BoxLayout):
    '''Application root widget '''
    taskholder = ObjectProperty()
    task_ids = ListProperty([])
    idscounter = NumericProperty(1)

    def load_tasks(self, *dt):
        '''Loads task data from data.json if exists.'''
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


# TODO Make undo when wrong data / take data from save?
    def set_time(self, instance, time, val, startdate, deadline):
        '''Set text value of 'time' object to delta time
        
        Parameters:
            instance (obj): object that calling function
            time (obj): reference to object that keeps
            val (bool): instance's 'on_focus' property value
            startdate (obj): reference to task startdate textinput
            deadline (obj): reference to task deadline textinput

        '''
        if not val:
            try:
                # convert dd:mm:yy to yy:mm:dd
                start = [int(x) for x in startdate.text.split('.')][::-1]
                end = [int(x) for x in deadline.text.split('.')][::-1]
                # create date object
                start = dates.date(*start)
                end = dates.date(*end)
            except (ValueError, TypeError):
                # TODO use regexp for wrong data
                print('You have entered wrong data')
                instance.do_undo()
            else:
                # find delta time
                res = dates.find_deltatime(start, end)   
                time.text = str(res)
                # return res

    def save_tasks(self, *args):
        ''' Save tasks to data.json
        '''
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
                # TODO Subtasks save
            }})
            print(data)
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(DATAFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def add_list_item(self):
        ''' Appends new task to taskholder widget'''
        widget = TASK.format(
            active=False, taskname='', priority='-',
            startdate=dates.convert_date(), time='', progress='0', deadline='',
            notes=''
        )
        self.taskholder.add_widget(Builder.load_string(widget))
        self.taskholder.children[0].popup.open()

    def add_subtask(self, instance):
        '''Adds subtask to task
        
        Parameters:
            instance (obj): reference to 'subtaskholder' object
        '''
        widget = SUBTASK.format(subactive=False, subtaskname='')
        instance.add_widget(Builder.load_string(widget))


class TempoApp(App):
    '''Main application class'''
    # icon = '../doc/sources/logo.png'
    icon = './doc/sources/logo2.png'
    def build(self):
        app = RootWidget()
        Clock.schedule_once(app.load_tasks)
        Clock.schedule_interval(app.save_tasks, 15)

        return app
