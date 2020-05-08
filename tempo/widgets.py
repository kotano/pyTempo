from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.lang.builder import Builder
from kivy.utils import platform
from kivy.properties import (
    DictProperty, ListProperty, NumericProperty,
    BooleanProperty, ObjectProperty, StringProperty)

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

from tempo import dates
from tempo.templates import (
    COLORS, SUBTASK, TASK, default_subtask,
    default_task, first_subtask)


class MyScreenManager(ScreenManager):
    fullscreen = False
    pass


class TaskScreen(Screen):
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
                'Deadline': x.deadline.text[::-1],  # FIXME
            }
            return which.get(instance.text, True)

        sorted_lst = sorted(lst, key=sort_criteria, reverse=True)
        if lst == sorted_lst:
            # UNDONE removed recursion
            sorted_lst = sorted(lst, key=sort_criteria, reverse=False)
        self.taskholder.children = sorted_lst

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

    def _clear_input(self, instance):
        '''Made to fix an unknown issue with
        clearing subtask text input
        instance (obj): subtask object reference
        '''
        instance.subtaskname.text = ''
        instance.subcheckbox.active = False

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

    pass


class TimerScreen(Screen):
    timerdisplay = ObjectProperty()
    POMODURATION = dates.POMODORO_DURATION
    count = NumericProperty(1)
    active = BooleanProperty(False)
    diff = ListProperty([POMODURATION, '00'])

    def trigger_countdown(self, task=None):
        if self.active is True:
            self.process.cancel()
            self.count = 1
            self.active = False
            return
        if not task:
            self.process = Clock.schedule_interval(
                lambda dt: self._track_time(self.POMODURATION), 1)
        else:
            self.process = Clock.schedule_interval(
                lambda dt: self._track_time(self.POMODURATION, task), 1)
        self.active = True

    def _track_time(self, value, task=None):
        total = (value * 60) - self.count
        if task:
            task._progress += 1/3600
            print(task._progress)
        if total == 0:
            self.trigger_countdown()
        mins = total // 60
        secs = total % 60
        self.diff = mins, secs
        self.count += 1

    def update(self):
        # print('Update timer')
        # print(self.counter)
        self.counter += 1
        pass


class CalendarScreen(Screen):
    pass


class DiaryScreen(Screen):
    pass


# WIDGETS
class Task(BoxLayout):
    deltatime = NumericProperty()
    _duration = NumericProperty()
    _max_duration = NumericProperty()
    _progress = NumericProperty()
    _in_progress = BooleanProperty(False)


class Subtask(Task):
    pass


class MiniTask(BoxLayout):
    _name = StringProperty()
    _source = ObjectProperty()


class PressableLabel(ButtonBehavior, Label):
    pass


class PressableBoxLayout(ButtonBehavior, BoxLayout):
    pass


class CustomScroll(ScrollView):
    if platform == 'win':
        effect_cls = ScrollEffect
    bar_color = COLORS['TempoBlue']
    pass
