from kivy.app import App
from kivy.graphics.instructions import Canvas
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class Task(BoxLayout):
    pass


class PriorityDropdown(BoxLayout):

    # def dropdown_open(self, button):

    pass


class RootWidget(BoxLayout):
    taskholder = ObjectProperty()
    task_ids = ListProperty([])

    def add_list_item(self):
        task = Task()
        self.taskholder.add_widget(task)


class TempoApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TempoApp().run()
