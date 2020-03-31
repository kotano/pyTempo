TASK = ('''
Task:
    id: task
    taskname: taskname.__self__
    priority: priority.__self__
    time: time.__self__
    deadline: deadline.__self__
    checkbox: checkbox.__self__
    
    popup: popup.__self__
    notes: notes.__self__
    startdate: startdate.__self__
    progress: progress.__self__

    
# checkbox
    CheckBox:
        id: checkbox
        active: {active}
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
                    TextInput:
                        id: taskname
                        text: '{taskname}'
                        write_tab: False
                        focus: True
                        hint_text: 'Enter task name'
                        multiline: False
                        size_hint: 0.8, 1

#> progress bar popup
                BoxLayout:
                    padding: 10, 10
                    size_hint_y: None
                    height: 50

#> task start date
                    TextInput:
                        id: startdate
                        size_hint_x: 0.25
                        text: '{startdate}'

#> progress bar
                    BoxLayout:
                        size_hint_x: 0.5
                        ListLabel:
                            id: progress
                            text: '{progress}'
                        ListLabel:
                            text: 'HOURS OF'
                        ListLabel:
                            id: time
                            text: '{time}'
#> deadline                    
                    TextInput:
                        size_hint_x: 0.25
                        id: deadline
                        text: '{deadline}'
                        
                
#> notes popup
                TextInput:
                    id: notes
                    text: '{notes}'
                    hint_text: 'Notes...'
                    size_hint: 1, 1
                    height: 100
                BoxLayout:
                    size_hint_y: None
                    height: 50
#> save button    
                    Button:
                        text: 'Save'
                        color: 0, 0, 0, 1
                        background_normal: ''
                        background_color: .70, .88, .87, 1
                        on_release: 
                            popup.dismiss();
                            app.root.save_tasks();
#> delete button
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
    ListLabel:
        text: priority.text

# timeline main
    ListLabel:
        text: time.text

# deadline main
    ListLabel:
        text: deadline.text
''')


SUBTASK = ('''
Task:
    id: subtask
    subtaskname: subtaskname.__self__
    checkbox: subcheckbox.__self__

    CheckBox:
        id: subcheckbox
        active: {subactive}
        size_hint: None, 1
        width: 20
        pos: root.center

    TextInput:
        id: subtaskname
        text: '{subtaskname}'
        write_tab: False
        focus: True
        hint_text: 'My new task!'
        multiline: False
        size_hint_x: 2
''')


if __name__ == "__main__":
    import tempo
    tempo.TempoApp().run()