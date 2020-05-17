import json
import os
from collections import OrderedDict

from kivy.app import App

from tempo.widgets import *  # noqa: F403

# NOTE: Can use KivyCalendar, if solve bug
# from KivyCalendar import CalendarWidget, DatePicker


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

    def find_delta(self, startdate, deadline):
        try:
            start = dates.convert_to_date(startdate.text)
            end = dates.convert_to_date(deadline.text)
        except (ValueError, TypeError):
            # TODO Make undo when wrong data / take data from save?
            print('You have entered wrong data')
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
        my_index = keep.index(
            [task.deltatime, task._duration, task._max_duration])
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

# XXX: ...
    # def start_countdown(self, task, mins):
    #     Clock.schedule_once(lambda dt: dates.countdown(mins))

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
                'progress': task._progress,
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

    def load_minitasks(self, holder):
        for x in self.taskholder.children:
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
        # Clock.schedule_interval(root.update_timer, 1)
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
