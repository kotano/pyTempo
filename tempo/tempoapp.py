if __name__ == "__main__":
    #! FOR DEBUGGING. REMOVE BEFORE Production
    import sys
    from os.path import dirname
    f = dirname(__file__)
    sys.path.append(f'{f}\\..')


import json
import os
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from tempo import dates
from tempo.templates import (SUBTASK, TASK, default_subtask, default_task,
                             first_subtask)


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
        except (FileNotFoundError):
            print('File does not exist. It will be created automatically.')
        else:
            for t in tasks.values():
                widget = TASK.format(
                    active=t['active'], taskname=t['taskname'],
                    priority=t['priority'],
                    startdate='.'.join(t['startdate']),
                    time=t['time'], progress=t['progress'],
                    deadline='.'.join(t['deadline']), notes=t['notes']
                )
                self.taskholder.add_widget(Builder.load_string(widget))
                for st in t['subtasks'][::-1]:
                    subtask = SUBTASK.format(
                        subactive=st[0], subtaskname=st[1], focus=False)
                    self.taskholder.children[0].subtaskholder.add_widget(
                        Builder.load_string(subtask))

    # TODO remove obsolete
    # def set_opacity(self, instance, value):
    #     '''If value is true, lower instance's opacity'''
    #     if value:
    #         return 
    #     else:
    #         instance.opacity = 1

    def complete_task(self, holder, root, value):
        '''Does task complete behavior

        Parameters:
            holder (obj): tasks container object
            root (obj): main task object
            value (bool): checkbox value
        '''
        # TODO archive, smooth animation
        if value:
            holder.remove_widget(root)
            holder.add_widget(root)

    def _clear_input(self, instance):
        '''Made to fix an unknown issue with
        clearing subtask text input
        instance (obj): subtask object reference
        '''
        instance.subtaskname.text = ''
        instance.subcheckbox.active = False

# TODO Make undo when wrong data / take data from save?
    def set_time(self, instance, time, val, startdate, deadline):
        '''Set text value of 'time' object to delta time
        
        Parameters:
            instance (obj): object that calling function
            time (obj): reference to object to place delta time value
            val (bool): instance's 'focus' property value
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
        ''' Save tasks to data.json'''
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
                'notes': task.notes.text.replace('\n', '\\n'),
                #! subtasks depend on structure. Not reliable
                'subtasks': [[s.children[2].active, s.children[1].text]
                for s in task.subtaskholder.children],
            }})
            print(data)
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(DATAFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def add_new_task(self):
        ''' Append new task to 'taskholder' widget'''
        self.taskholder.add_widget(Builder.load_string(default_task))
        last_task = self.taskholder.children[0]
        subtskhldr = last_task.subtaskholder
        subtskhldr.add_widget(Builder.load_string(first_subtask))
        last_task.popup.open()

    def add_subtask(self, holder):
        '''Adds subtask to task
        
        Parameters:
            holder (obj): reference to 'subtaskholder' object
        '''
        holder.add_widget(Builder.load_string(default_subtask))


class TempoApp(App):
    '''Main application class'''
    icon = './docs/sources/icon_white.png'
    def build(self):
        app = RootWidget()
        Clock.schedule_once(app.load_tasks)
        Clock.schedule_interval(app.save_tasks, 15)

        return app


# FOR DEBUG
if __name__ == "__main__":
    TempoApp().run()