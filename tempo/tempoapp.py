if __name__ == "__main__":
    #! FOR DEBUGGING. REMOVE BEFORE PRODUCTION
    import sys
    from os.path import dirname
    f = dirname(__file__)
    sys.path.append(f'{f}\\..')


import json
import os
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.lang.builder import Builder
from kivy.properties import (DictProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from tempo import dates
from tempo.templates import (COLORS, SUBTASK, TASK, default_subtask,
                             default_task, first_subtask)

# NOTE: Can use KivyCalendar, if solve bug
# from KivyCalendar import CalendarWidget, DatePicker


class Task(BoxLayout):
    deltatime = NumericProperty(12)
    _duration = NumericProperty()
    _max_duration = NumericProperty()
    
    COLORS = DictProperty(COLORS)
    pass

class Subtask(Task):
    pass

class MiniTask(BoxLayout):
    _name = StringProperty()
    _source = ObjectProperty()

class PressableLabel(ButtonBehavior, Label):
    pass

class PressableBoxLayout(ButtonBehavior, BoxLayout):
    pass

class MyScreenManager(ScreenManager):
    fullscreen = False
    pass

class TaskScreen(Screen):
    pass

class TimerScreen(Screen):
    pass


class CustomScroll(ScrollView):
    if platform == 'win':
        effect_cls = ScrollEffect
    bar_color = COLORS['TempoBlue']
    pass


class RootWidget(BoxLayout):
    '''Application root widget '''
    taskholder = ObjectProperty()
    minitaskholder = ObjectProperty()
    COLORS = DictProperty(COLORS)


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
                    duration=t['duration'], progress=t['progress'],
                    deadline='.'.join(t['deadline']), notes=t['notes']
                )
                self.taskholder.add_widget(Builder.load_string(widget))
                for st in t['subtasks'][::-1]:
                    subtask = SUBTASK.format(
                        subactive=st[0], subtaskname=st[1], focus=False)
                    self.taskholder.children[0].subtaskholder.add_widget(
                        Builder.load_string(subtask))
        except (FileNotFoundError):
            print('File does not exist. It will be created automatically.')
        except (KeyError, json.JSONDecodeError) as e:
            # Except error in case of data corruption
            msg = (str(e) + 'We were unable to load data.'
            'Would you like to delete this task? [y/n]')
            q = input(msg)
            if not q.lower() == 'y':
                app.stop() 
 

    def complete_task(self, holder, root, value):
        '''Does task complete behavior

        Parameters:
            holder (obj): tasks container object
            root (obj): main task object
            value (bool): checkbox value
        '''
        # TODO: Archive, smooth animation
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

    def sort_tasks(self, instance):
        '''Sort tasks in tasklist.
        
        Parameters:
            instance (obj): caller
        '''
        lst = self.taskholder.children
        if len(lst) <= 1:
            print('Nothing to sort')
            return


        def sort_criteria(x):
            which = {
            'Taskname': x.taskname.text, 
            'Priority': x.priority.text,
            'Duration': x.duration.text,
            'Deadline': x.deadline.text[::-1], # FIXME
            }
            return which.get(instance.text, True)

        sorted_lst = sorted(lst, key=sort_criteria, reverse=True)
        if lst == sorted_lst:
            # UNDONE removed recursion
            sorted_lst = sorted(lst, key=sort_criteria, reverse=False)
        self.taskholder.children = sorted_lst



    def find_delta(self, startdate, deadline):
        try:
            start = dates.convert_to_date(startdate.text)
            end = dates.convert_to_date(deadline.text)
        except (ValueError, TypeError):
            # TODO Make undo when wrong data / take data from save?
#            print('You have entered wrong data')
            return 0
        else:
            # find delta time
            res = dates.find_deltatime(start, end)
            return res


    def find_max_duration(self, task):
        '''Find maximum available time for each task and return int.'''
        # TODO: This needs optimization
        keep = []
        for t in self.taskholder.children:
            keep.append([t.deltatime, t._duration, t._max_duration])
        keep = sorted(keep, key=lambda x: x[0])
        my_index = keep.index([task.deltatime, task._duration, task._max_duration])
        after = [x[2] for x in keep][my_index:]
        before = [x[1] for x in keep][:my_index]
        # NOTE: can add +1 to before slice to remove task._duration
        max_duration = task.deltatime - task._duration - sum(before)
        if min(after) != 0:
            max_duration = min(max_duration, min(after))
        max_duration = max(0, max_duration)
        task._max_duration = max_duration
        # print(task._max_duration)
        return max_duration

    def refresh_data(self, *dt):
        # XXX: Bad solution
        if len(self.minitaskholder.children) == 0:
            self.load_minitasks(self.minitaskholder)
        for t in self.taskholder.children:
            t.deltatime = self.find_delta(t.startdate, t.deadline)
        for t in self.taskholder.children:
            t.duration.hint_text = str(self.find_max_duration(t))
            # HACK ...
            t._duration = t.duration.text if t.duration.text else 0


    def save_tasks(self, *dt):
        ''' Save tasks to data.json'''
        data = {}
        counter = 1
        for task in self.taskholder.children[::-1]:
            data.update({counter: {
                'active': task.checkbox.active,
                'taskname': task.taskname.text,
                'priority': task.priority.text,
                'startdate': task.startdate.text.split('.'),
                'duration': task.duration.text,
                'progress': task.progress.text,
                'deadline': task.deadline.text.split('.'),
                'notes': task.notes.text.replace('\n', '\\n'),
                # XXX: subtasks depend on structure. Not reliable
                'subtasks': [[s.children[2].active, s.children[1].text]
                for s in task.subtaskholder.children],
            }})
            # print(data)
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

    def load_minitasks(self, holder):
        for x in self.taskholder.children:
            print(x)
            widget = MiniTask()
            widget._source = x
            widget._name = x.taskname.text
            holder.add_widget(widget)

class TempoApp(App):
    '''Main application class'''
    icon = './docs/sources/icon_white.png'
    def on_stop(self):
        self.root.save_tasks()
        return True

    def build(self):
        root = RootWidget()
        Clock.schedule_once(root.load_tasks)
        Clock.schedule_once(root.refresh_data, 2)
        Clock.schedule_interval(root.refresh_data, 5)
        Clock.schedule_interval(root.save_tasks, 45)
        return root

# Multiplatform path to application user data 
DATAFILE = os.path.join(TempoApp().user_data_dir, 'data.json')


# FOR DEBUG
if __name__ == "__main__":
    application = TempoApp()
    application.run()
