
from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.lang.builder import Builder
from kivy.properties import (DictProperty, ListProperty, NumericProperty, BooleanProperty, ObjectProperty, StringProperty)
from kivy.utils import platform

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
from tempo.templates import (COLORS, SUBTASK, TASK, default_subtask,
                             default_task, first_subtask)



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

class MyScreenManager(ScreenManager):
    fullscreen = False
    pass

class TaskScreen(Screen):
    pass

class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.c = Clock.schedule_interval(lambda dt: self.update(), 1)
        self.counter = 1
    def update(self):
        # print('Update timer')
        # print(self.counter)
        self.counter += 1
        pass

class CalendarScreen(Screen):
    pass

class DictionaryScreen(Screen):
    pass

class CustomScroll(ScrollView):
    if platform == 'win':
        effect_cls = ScrollEffect
    bar_color = COLORS['TempoBlue']
    pass
