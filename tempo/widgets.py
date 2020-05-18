from kivy.factory import Factory
from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.lang.builder import Builder
from kivy.utils import platform
from kivy.properties import (
    DictProperty, ListProperty, NumericProperty,
    BooleanProperty, ObjectProperty, StringProperty, Property)

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
    POMODURATION = NumericProperty(dates.POMODORO_DURATION)
    count = NumericProperty(1)
    active = BooleanProperty(False)
    angle = NumericProperty(360)
    display = ListProperty([POMODURATION.defaultvalue, '00'])
    current_task = None

    def trigger_countdown(self, task=current_task):
        self.current_task = task
        if self.active is True:
            self.process.cancel()
            self.active = False
            return
        if not task:
            self.process = Clock.schedule_interval(
                lambda dt: self._track_time(self.POMODURATION), 1)
        else:
            self.process = Clock.schedule_interval(
                lambda dt: self._track_time(self.POMODURATION, task), 1)
        self.active = True

    def _stop_timer(self):
        if self.active is True:
            self.process.cancel()
            self.active = False
            self.current_task = None
            self.count = 1
            self.angle = 360
            self.display = [self.POMODURATION, '00']

    def _track_time(self, value, task=None):
        total = (value * 60) - self.count
        print(total)
        if task:
            task._progress += 1/3600
            print(task._progress)
        if total == 0:
            self._stop_timer()
        mins = total // 60
        secs = total % 60
        self.display = mins, secs
        self.angle = self._circle()
        self.count += 1

    def _circle(self):
        step = (self.POMODURATION * 60) / 360
        res = self.count // step
        return res


class CalendarScreen(Screen):
    pass


class DiaryScreen(Screen):
    pass


# WIDGETS
class Task(BoxLayout):
    _duration = NumericProperty()
    _max_duration = NumericProperty()
    _progress = NumericProperty()
    
    deltatime = NumericProperty()
    in_progress = BooleanProperty(False)


class Subtask(Task):
    pass


class MiniTask(BoxLayout):
    _name = StringProperty()
    _source = ObjectProperty()


# class PressableLabel(ButtonBehavior, Label, Button):
class PressableLabel(Button):
    pass


class PressableBoxLayout(ButtonBehavior, BoxLayout):
    pass


class CustomScroll(ScrollView):
    if platform == 'win':
        effect_cls = ScrollEffect
    bar_color = COLORS['TempoBlue']
    pass


class LongpressButton(Factory.Button):
    __events__ = ('on_long_press',)

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.disabled = True
        self.state = 'normal'
        Clock.schedule_once(self._unblock, 1)
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def _unblock(self, dt):
        self.disabled = False
# btn = LongpressButton(
#             long_press_time=3,
#             on_press=lambda w: setattr(w, 'text', 'short press!'),
#             on_long_press=lambda w: setattr(w, 'text', 'long press!'))
