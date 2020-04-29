from tempo import dates

TASK = ('''
Task:
    id: task
    taskname: taskname.__self__
    priority: priority.__self__
    checkbox: checkbox.__self__
    subtaskholder: subtaskholder.__self__
    
    popup: popup.__self__
    startdate: startdate.__self__
    progress: progress.__self__
    time: time.__self__
    deadline: deadline.__self__
    notes: notes.__self__

    opacity: .2 if checkbox.active else 1
    
# checkbox
    CheckBox:
        id: checkbox
        active: {active}
        on_active: app.root.complete_task(root.parent, root, self.active)
        size_hint: None, 1
        width: 20
        pos: root.center
    
# TASKNAME # POPUP
    BoxLayout:
        size_hint_x: 2
        id: bl

#> popup
        Popup:
            id: popup
            size_hint: 0.9, 0.9
            title: "Edit task"
            # background_color: 1, 1, 1, 1
            on_parent:
                if self.parent == bl: self.parent.remove_widget(self)
            on_dismiss: if not any((taskname.text, deadline.text, notes.text)): app.root.taskholder.remove_widget(task)
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                background_color: 1, 1, 1, 1
                orientation: 'vertical'


                BoxLayout:
                    size_hint: 1, None
                    height: 50
                    spacing: 40, 40
#> priority popup
                    PrioritySpinner:
                        size_hint: 0.1, 1
                        id: priority
                        text: '{priority}'

#> task name popup
                    DefaultInput:
                        id: taskname
                        text: '{taskname}'
                        font_size: 18
                        focus: True
                        hint_text: 'Enter task name'
                        size_hint: 0.8, 1

#> timeline
                BoxLayout:
                    canvas.before:
                        Color:
                            rgba: .5, .5, .5, 1
                        Line:
                            width: 1
                            rectangle: self.x, self.y, self.width, self.height
                    padding: 10, 10
                    size_hint_y: None
                    height: 50

#> task start date
                    DateInput:
                        id: startdate
                        size_hint_x: 0.25
                        text: '{startdate}'
                        on_focus: 
                            app.root.set_time(self, time, self.focus, startdate, deadline)

#> progress bar
                    BoxLayout:

                        size_hint_x: 0.5
                        BlackLabel:
                            id: progress
                            text: '{progress}'
                        BlackLabel:
                            text: 'HOURS OF'
                        BlackLabel:
                            id: time
                            text: '{time}'

#> deadline          
                    DateInput:
                        size_hint_x: 0.25
                        id: deadline
                        text: '{deadline}'
                        on_focus: 
                            app.root.set_time(self, time, self.focus, startdate, deadline)
                        # on_focus: self.text = app.set_time(startdate.text, deadline.text)

#> Subtask
                GridLayout:
                    id: subtaskholder
                    cols: 1
#> notes
                AnchorLayout:
                    anchor_x: 'center'
                    DefaultInput:
                        canvas.after:
                            Color:
                                rgba: 0, 0, 0, 1
                            Line:
                                width: 1
                                rectangle: self.x, self.y, self.width, self.height 
                        id: notes
                        text: '{notes}'
                        multiline: True
                        hint_text: 'Notes...'
                        size_hint: 0.9, 0.9
                        # height: 100
#> footer
                BoxLayout:
                    size_hint_y: None
                    height: 50
#>> save button    
                    Button:
                        text: 'Save'
                        color: 0, 0, 0, 1
                        background_normal: ''
                        background_color: .70, .88, .87, 1
                        on_release: 
                            app.root.save_tasks();
                            popup.dismiss();
#>> delete button
                    Button:
                        text: 'Delete'
                        # min_state_time: 1
                        trigger_action: 5
                        size_hint_x: None
                        width: 50
                        background_color: 1, 0, 0, 1
                        on_release:
                            app.root.taskholder.remove_widget(task);
                            popup.dismiss();
                            app.root.save_tasks();

# task name button
        Button:
            background_normal: ''
            color: 0, 0, 0, 1
            text: taskname.text
            on_release: root.popup.open()

# priority main
    BlackLabel:
        text: priority.text

# time main
    BlackLabel:
        text: time.text

# deadline main
    BlackLabel:
        text: deadline.text
''')


SUBTASK = ('''
Subtask:
    id: subtask
    subtaskname: subtaskname.__self__
    subcheckbox: subcheckbox.__self__
    
    opacity: .2 if subcheckbox.active else 1

    CheckBox:
        id: subcheckbox
        active: {subactive}
        size_hint: None, 1
        width: 20
        pos: root.center
        on_active: app.root.complete_task(root.parent, root, self.active)

    TextInput:
        id: subtaskname
        text: '{subtaskname}'
        size_hint_x: 0.9
        background_normal: ''
        hint_text: 'Create new subtask'
        multiline: False
        write_tab: False
        focus: {focus}
        # on_focus: subtask.opacity=1
        on_text_validate: app.root.add_subtask(root.parent)
    
    Button:
        size_hint: None, None
        width: 32
        height: 32
        color: 0, 0, 0, .5
        background_normal: './docs/sources/delete32.png'
        on_release: app.root._clear_input(subtask) if len(root.parent.children) <= 1 else root.parent.remove_widget(subtask)
''')


default_task = TASK.format(
            active=False, taskname='', priority='-',
            startdate=dates.convert_date(), time='', progress='0', deadline='',
            notes=''
        )


default_subtask = SUBTASK.format(subactive=False, subtaskname='', focus = True)
first_subtask = SUBTASK.format(subactive=False, subtaskname='', focus = False)