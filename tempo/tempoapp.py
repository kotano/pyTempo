import json
import os
from collections import OrderedDict

from kivy.app import App

from tempo import config
from tempo.widgets import *  # noqa: F403

# NOTE: Can use KivyCalendar, if solve bug
# from KivyCalendar import CalendarWidget, DatePicker


# >>> App <<<
class RootWidget(BoxLayout):
    '''Application root widget '''
    diaryscreen = ObjectProperty()

    storyholder = ObjectProperty()
    taskholder = ObjectProperty()
    minitaskholder = ObjectProperty()
    COLORS = DictProperty(COLORS)

    def print_message(self, msg, duration=3):
        '''Temporarily display message on action bar'''
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
            start = dates.convert_to_date(startdate.text)
            end = dates.convert_to_date(deadline.text)
        except (ValueError, TypeError) as e:
            print(e)
            # TODO: Make undo when wrong data / take data from save?
            print('You have entered wrong data')
            return 0
        else:
            # Find delta time
            hours = dates.find_deltatime(start, end)
            worktime = dates.find_worktime(hours)
            return worktime

    # NOTE: This func is disabled due to restructuring of the applictaion.
    def find_max_duration(self, task):
        '''Find maximum available time for each task and return int.

            This code is a part of application main algorithm.
            It may be hard for understanding
             if you don't have an idea how it should work.
        '''
        # XXX: UNSTABLE
        # TODO: This needs optimization
        # FIXME: Unpredictable results
        keep = []
        for t in self.taskholder.children:
            keep.append([t.deltatime, t._duration, t._max_duration])
        keep = sorted(keep, key=lambda x: x[0])
        my_index = keep.index(
            [task.deltatime, task._duration, task._max_duration])
        before = [x[1] for x in keep][:my_index]
        after = [x[2]-x[1] for x in keep][my_index+1:]
        max_duration = task.deltatime - sum(before)
        if after:
            max_duration = min(max_duration, min(after))
        max_duration = max(0, max_duration)
        task._max_duration = max_duration
        return max_duration

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
                widget = TASK.format(
                    active=t['active'],
                    taskname=t['taskname'],
                    priority=t['priority'],
                    startdate='.'.join(t['startdate']),
                    duration=t['duration'],
                    progress=t['progress'],
                    deadline='.'.join(t['deadline']),
                    notes=t['notes']
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
                   'Would you like to delete this tasks? [y/n]')
            q = input(msg)
            if not q.lower() == 'y':
                applic.stop()

    def save_tasks(self, *dt):
        ''' Save tasks to .json file'''
        data = {}
        counter = 1
        for task in self.taskholder.children[::-1]:
            data.update({counter: {
                'active': task.checkbox.active,
                'taskname': task.taskname.text,
                'priority': task.priority.text,
                'startdate': task.startdate.text.split('.'),
                'duration': task.duration.text,
                'progress': task._progress,
                'deadline': task.deadline.text.split('.'),
                'notes': task.notes.text.replace('\n', '\\n'),
                # XXX: subtasks depend on structure. Not reliable
                'subtasks': [[s.children[2].active, s.children[1].text]
                             for s in task.subtaskholder.children],
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
            # Add new items to holder
            if x in minilist:
                continue
            holder.add_widget(_make_mini(x))

        for x in holder.children:
            # Remove old items from holder
            if x._source not in tasklist:
                holder.remove_widget(x)

    def populate_completed_tasks(self, holder):
        # XXX

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

        for x in holder.children:
            # Remove old items from holder
            if x._source not in tasklist:
                holder.remove_widget(x)

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
                    # completed='.'.join(t['startdate']),
                )
                strhld = self.storyholder
                strhld.add_widget(Builder.load_string(widget))
                # for st in t['subtasks'][::-1]:
                #     subtask = SUBTASK.format(
                #         subactive=st[0], subtaskname=st[1], focus=False)
                #     self.taskholder.children[0].subtaskholder.add_widget(
                #         Builder.load_string(subtask))
        except (FileNotFoundError):
            print('File does not exist. It will be created automatically.')
        except (KeyError, json.JSONDecodeError) as e:
            # Except error in case of data corruption
            msg = (str(e) + 'We were unable to load data.'
                   'Would you like to delete all data? [y/n]')
            q = input(msg)
            if not q.lower() == 'y':
                applic.stop()

    def save_stories(self, *dt):
        ''' Save stories to .json file'''
        data = {}
        counter = 1
        for story in self.storyholder.children[::-1]:
            data.update({counter: {
                'storytext': story._text,
                'postnum': story.postnum,
                'creation': story.creation,
                'storytext': story._text.replace('\n', '\\n'),
                # 'completed_tasks': [[s.children[2].active, s.children[1].text]
                #              for s in task.subtaskholder.children],
            }})
            counter += 1
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        with open(STORYFILE, 'w+', encoding='utf-8') as storyfile:
            json.dump(data, storyfile, indent=4)


class TempoApp(App):
    '''Main application class'''
    icon = './data/icons/icon_white.png'

    def on_stop(self):
        # Save tasks before exit
        self.root.save_tasks()
        self.root.save_stories()
        return True

    def build(self):
        global applic
        applic = self
        root = RootWidget()
        Clock.schedule_once(root.load_tasks, 0.1)
        Clock.schedule_once(root.load_stories, 0.1)
        Clock.schedule_interval(root.save_tasks, 45)
        Clock.schedule_interval(root.save_stories, 45)
        return root


# Multiplatform path to application user data
datadir = TempoApp().user_data_dir
TASKFILE = os.path.join(datadir, 'tasks.json')
STORYFILE = os.path.join(datadir, 'stories.json')


# FOR DEBUG
if __name__ == "__main__":
    application = TempoApp()
    application.run()
