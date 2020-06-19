import json
from os import path
from collections import OrderedDict

from kivy.uix.widget import Widget

from tempo import utils
from tempo.settings import ConfiguredApp
from tempo.templates import TASK, SUBTASK
from tempo.widgets import *  # noqa: F403

if path.exists('./tempo/tempo_algorithm/algorithm.py'):
    print('YES')
else:
    print('NO')


class RootWidget(BoxLayout):
    '''Application root widget '''
    content_window = ObjectProperty()
    diaryscreen = ObjectProperty()

    storyholder = ObjectProperty()
    taskholder = ObjectProperty()
    minitaskholder = ObjectProperty()
    COLORS = DictProperty(COLORS)

    def switch_screen(self, screen):
        """Safely trigger screen change.

        Args:
            screen ([str, int]): Screen name or position on the sidebar.
        """
        if screen == 'taskscreen' or screen == 1:
            self.ids.taskscreen_button.trigger_action()
        elif screen == 'timerscreen' or screen == 2:
            self.ids.timerscreen_button.trigger_action()
        elif screen == 'calendarscreen' or screen == 3:
            self.ids.calendarscreen_button.trigger_action()
        elif screen == 'diaryscreen' or screen == 4:
            self.ids.diaryscreen_button.trigger_action()

    def print_message(self, msg, duration=3):
        '''Temporarily display message on action bar.'''
        def _set_title(m):
            self.ids.actiontitle.title = m

        prev = self.ids.actiontitle.title
        # TODO: Make safe intersection of two messages
        Clock.schedule_once(lambda dt: _set_title(prev), duration)
        _set_title(msg)

    def collect_height(self, instance, extra=0):
        total = sum([c.height+extra for c in instance.children])
        print('children height', total)
        return total

    def get_worktime(self, startdate, deadline):
        '''Compute full work time for task and handle exceptions. Return int.

            Parameters:
                startdate(obj): Task startdate textinput object
                deadline(obj): Task deadline textinput object
        '''
        try:
            start = utils.convert_to_date(startdate.text)
            end = utils.convert_to_date(deadline.text)
        except (ValueError, TypeError) as e:
            print(e)
            # TODO: Make undo when wrong data / take data from save?
            print('You have entered wrong data')
            return 0
        else:
            # Find delta time
            hours = utils.find_deltatime(start, end)
            worktime = utils.find_worktime(hours, self.APP.worktime)
            return worktime

    # NOTE: This func is disabled due to restructuring of the applictaion.

    # def refresh_data(self, *dt):
    #     for t in self.taskholder.children:
    #         t.deltatime = self.get_worktime(t.startdate, t.deadline)
    #     for t in self.taskholder.children:
    #         t.duration.hint_text = str(self.find_max_duration(t))
    #         # HACK ...
    #         t._duration = t.duration.text if t.duration.text else 0

    def load_tasks(self, *dt):
        '''Loads task data from data.json if exists.'''
        try:
            with open(TASKFILE, 'r') as datafile:
                tasks = json.load(datafile)
            for t in tasks.values():
                widget = Task()
                widget.load_data(t)
                self.taskholder.add_widget(widget)
        except (FileNotFoundError):
            msg = 'File does not exist. It will be created automatically.'
            self.print_message(msg, 10)
            print(msg)
        except (KeyError, json.JSONDecodeError) as e:
            # Except error in case of data corruption
            msg = (str(e) + 'We were unable to load data. '
                   'Would you like to delete this tasks? [y/n]')
            self.print_message(msg, 10)
            q = input(msg)
            if not q.lower() == 'y':
                self.APP.stop()

    def save_tasks(self, *dt):
        ''' Save tasks to .json file'''
        data = {}
        counter = 1
        for task in self.taskholder.children[::-1]:
            data.update({counter: {
                **task.save_data()
            }})
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(TASKFILE, 'w+', encoding='utf-8') as datafile:
            json.dump(data, datafile, indent=4)

    def populate_minitasks(self, holder):
        '''Populate minitaskholder on timer screen using
        original tasks from taskholder.
        '''
        tasklist = self.taskholder.children
        minilist = [x._source for x in holder.children]

        def _make_mini(src):
            # Create minitask element with reference to source task
            widget = MiniTask()
            widget._source = src
            widget._name = src.taskname.text
            return widget

        for x in tasklist[::-1]:
            print(x)
            # Add new items to holder
            if x in minilist:
                continue
            holder.add_widget(_make_mini(x))

        for x in holder.children:
            # Remove old items from holder
            if x._source not in tasklist:
                holder.remove_widget(x)

    def populate_completed_tasks(self, holder):
        # TODO: Refactor

        tasklist = self.taskholder.children
        storylist = [x._source for x in holder.children]

        def _make_completed(task):
            widget = CompletedTask()
            widget._source = task
            widget._text = task.taskname.text
            widget._data = task.save_data()
            return widget

        for t in tasklist[::-1]:
            # Add new items to holder
            if t in storylist:
                continue
            if t.checkbox.active:
                holder.add_widget(_make_completed(t))

    def load_stories(self, *dt):
        '''Loads story data from data.json if exists.'''
        try:
            with open(STORYFILE, 'r') as storyfile:
                stories = json.load(storyfile)
            for s in stories.values():
                widget = STORY.format(
                    postnum=s['postnum'],
                    creation=s['creation'],
                    storytext=s['storytext'],
                    completed_tasks=s['completed_tasks'],
                )
                strhld = self.storyholder
                strhld.add_widget(Builder.load_string(widget))
        except (FileNotFoundError):
            print('File does not exist. It will be created automatically.')
        except (KeyError, json.JSONDecodeError) as e:
            # Except error in case of data corruption
            msg = (str(e) + 'We were unable to load data.'
                   'Would you like to delete all data? [y/n]')
            q = input(msg)
            if not q.lower() == 'y':
                self.APP.stop()

    def save_stories(self, *dt):
        ''' Save stories to .json file'''
        data = {}
        counter = 1
        for story in self.storyholder.children[::-1]:
            data.update({counter: {
                **story.save_data()
            }})
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(STORYFILE, 'w+', encoding='utf-8') as storyfile:
            json.dump(data, storyfile, indent=4)


class TempoApp(ConfiguredApp):
    '''Tempo application class.

    This class inherits from ConfiguredApp class
    which sets app settings configuration.
    '''
    pomoduration = NumericProperty()
    pomorest = NumericProperty()
    worktime = NumericProperty()

    icon = './data/icons/icon_white.png'

    def on_stop(self):
        """Save data before exit."""
        # self.remember_window()
        self.root.save_tasks()
        self.root.save_stories()

    def build(self):
        Widget.APP = self
        # Set application attributes stored in tempo.ini
        # see parent class for more info.
        self.configure_app()
        root = RootWidget()
        Clock.schedule_once(root.load_tasks, 0.1)
        Clock.schedule_once(root.load_stories, 0.1)
        Clock.schedule_interval(root.save_tasks, 45)
        Clock.schedule_interval(root.save_stories, 45)
        Clock.schedule_interval(self.remember_window, 20)
        return root


# Multiplatform path to application user data
datadir = TempoApp().user_data_dir
TASKFILE = path.join(datadir, 'tasks.json')
STORYFILE = path.join(datadir, 'stories.json')


# FOR DEBUG
if __name__ == "__main__":
    application = TempoApp()
    application.run()
