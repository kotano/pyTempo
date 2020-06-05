import calendar
# from math import ceil

from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty, DictProperty, ListProperty,
    NumericProperty, ObjectProperty, Property,
    StringProperty)
from kivy.uix.actionbar import ActionBar
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.utils import platform

from tempo.tempoapp import App
from tempo import dates
from tempo.templates import (
    COLORS, STORY, SUBTASK, TASK,
    default_subtask, default_task, first_subtask)


# >>> WIDGETS <<<
class Box(BoxLayout):
    pass


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
        Clock.schedule_once(self._unblock, 0.5)
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def _unblock(self, dt):
        self.disabled = False


# >>> SCREENS <<<
class MyScreenManager(ScreenManager):
    fullscreen = False
    pass


# TASKS
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
        if value:
            holder.remove_widget(root)
            holder.add_widget(root)


class Task(BoxLayout):
    _duration = NumericProperty()
    _max_duration = NumericProperty()
    _progress = NumericProperty()

    deltatime = NumericProperty()
    in_progress = BooleanProperty(False)

    _data = DictProperty()

    def save_data(self):
        data = {
            'active': self.checkbox.active,
            'taskname': self.taskname.text,
            'priority': self.priority.text,
            'startdate': self.startdate.text.split('.'),
            'duration': self.duration.text,
            'progress': self._progress,
            'deadline': self.deadline.text.split('.'),
            'notes': self.notes.text.replace('\n', '\\n'),
            # XXX: subtasks depend on structure. Not reliable
            'subtasks': [[s.children[2].active, s.children[1].text]
                            for s in self.subtaskholder.children],
        }
        self._data = data
        return data


class Subtask(Task):
    pass


# TIMER
class TimerScreen(Screen):
    timerdisplay = ObjectProperty()
    minitaskholder = ObjectProperty()
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
        self.process = Clock.schedule_interval(
            lambda dt: self._track_time(self.POMODURATION, task), 1)
        self.active = True

    def stop_timer(self):
        if self.active is True:
            self.process.cancel()
            self.angle = 360
            self.active = False
            self.current_task = None
            self.count = 1
            self.display = [self.POMODURATION, '00']
            self._reset_minitasks_state()

    def _track_time(self, value, task=None):
        total = (value * 60) - self.count
        # print(total)
        if task:
            task._progress += 1/3600
            # print(task._progress)
        if total == 0:
            self.stop_timer()
            return
        mins = total // 60
        secs = total % 60
        self.display = mins, secs
        self.angle = self._circle()
        self.count += 1

    def _circle(self):
        step = (self.POMODURATION * 60) / 360
        res = self.count // step
        return res

    def _reset_minitasks_state(self):
        for t in self.minitaskholder.children:
            for b in t.children:
                b.state = 'normal'


class MiniTask(BoxLayout):
    _name = StringProperty()
    _source = ObjectProperty()


# CALENDAR
class CalendarScreen(Screen):
    pass


class CalendarView(Label):
    cal = calendar.TextCalendar(0)
    endar = cal.formatmonth(dates.cur_year, dates.cur_month)
    c = StringProperty(endar)


# DIARY
class DiaryScreen(Screen):
    storyholder = ObjectProperty()
    storylist = ListProperty()
    storycount = NumericProperty(1)

    def count_postnum(self):
        lst = [0, ]
        for x in self.storyholder.children:
            lst.append(x.postnum)
        r = max(lst) + 1
        self.storycount = r

    def undo_story(self, instance):
        self.storyholder.remove_widget(instance)
        self.storycount -= 1

    def add_story(self, isnew=True):
        self.count_postnum()
        widget = STORY.format(
            postnum=self.storycount,
            creation=dates.date_to_list(),
            storytext='',
        )
        self.storyholder.add_widget(
            Builder.load_string(widget),
            index=len(self.storyholder.children))
        self.storyholder.children[-1].ids.popup.open()
        # self.storyholder.add_widget(Builder.load_string(STORY))


class Storyholder(GridLayout):

    def collect_height(self, instance, extra=0):
        total = sum([c.height+extra for c in instance.children])
        print('children height', total)
        return total


class Story(Box):
    '''Story widget'''
    # completed_tasks = ObjectProperty()

    fullheight = NumericProperty()
    creation = ListProperty()
    postnum = NumericProperty()
    _text = StringProperty()
    _title = StringProperty()

    # def refresh_values(self):
    #     set_title()
    #     refresh()
    #     pass

    def _set_title(self):
        self._title = self._text.split('\n')[0][:20]

    def _set_height(self, *dt):
        par = self.parent
        if not par:
            return
        height = sum([x.height for x in self.children])
        self.height = height
        par.height = par.collect_height(par, 50)

    def add_completed(self):
        pass

    def refresh(self):
        default = 100
        self._set_title()
        self.arrange_completed(self.ids['completed_tasks'])

        Clock.schedule_once(self._set_height, 0.1)
        return default
        # print('Refreshing height...', height)

    def arrange_completed(self, instance):
        # instance = self.ids.completed_tasks
        height = instance.children[0].height if instance.children else 30

        def _set_vals(*dt):
            total_width = sum([x.width for x in instance.children])
            rows = total_width / instance.width
            r = height * (int(rows) * 2) if rows > 1 else height
            instance.height = r
        Clock.schedule_once(_set_vals, 0.1)
        return height


class CompletedTask(ToggleButton):
    _source = ObjectProperty()
    _text = StringProperty()

    pass
