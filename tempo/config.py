# Disable multitouch on Windows
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.settings import SettingsWithTabbedPanel, SettingsWithSidebar
from kivy.app import App
from kivy.utils import platform
from kivy.core.window import Window
import json

debug = True

if platform == 'win':
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('kivy', 'exit_on_escape', '0')

    # if debug is True:
    # print(Window.left)
    # print(Window.top)
    # Window.left = 0
    # Window.top = -800


"""
Config Example
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

When the user next runs the programs, their changes are restored.

"""


# We first define our GUI
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Configure app (or press F1)'
        on_release: app.open_settings()
    Label:
        id: label
        text: 'Hello'
'''

# This JSON defines entries we want to appear in our App configuration screen
mylable = '''
[
    {
        "type": "string",
        "title": "Label caption",
        "desc": "Choose the text that appears in the label",
        "section": "My Label",
        "key": "text"
    },
    {
        "type": "numeric",
        "title": "Label font size",
        "desc": "Choose the font size the label",
        "section": "My Label",
        "key": "font_size"
    }
]
'''

pomodoro = '''
[
    {
        "type": "numeric",
        "title": "Pomodoro duration",
        "desc": "Choose the duration of pomodoro work time",
        "section": "Pomodoro",
        "key": "pomodoro_duration"
    },
    {
        "type": "numeric",
        "title": "Pomodoro rest",
        "desc": "Choose the pomodoro rest time",
        "section": "Pomodoro",
        "key": "pomodoro_rest"
    }
]
'''

window = '''
[
    {
        "type": "numeric",
        "title": "Window left position",
        "desc": "Choose the window left edge position",
        "section": "Window",
        "key": "left"
    },
    {
        "type": "numeric",
        "title": "Window top position",
        "desc": "Choose the window top edge position",
        "section": "Window",
        "key": "top"
    },

]
'''

with open('config.json') as f:
    configs = json.load(f)

POMODORO_DURATION = 25
POMODORO_REST = 5
HOURSPERDAY = 6


class ConfiguredApp(App):

    settings_cls = SettingsWithSidebar

    # def build(self):
    #     """
    #     Build and return the root widget.
    #     """
    # The line below is optional. You could leave it out or use one of the
    # standard options, such as SettingsWithSidebar, SettingsWithSpinner
    # etc.
    # self.settings_cls = MySettingsWithTabbedPanel

    # We apply the saved configuration settings or the defaults
    # Window.left = self.config.get('Window', 'left')
    # Window.top = self.config.get('Window', 'top')
    # # Window.left = 0
    # # Window.top = -800
    # root = Builder.load_string(kv)
    # label = root.ids.label
    # label.text = self.config.get('My Label', 'text')
    # label.font_size = float(self.config.get('My Label', 'font_size'))
    # return root

    def set_window(self):
        self._set_window_pos()
        # self._set_window_size()

    def _set_window_pos(self):
        Window.left = int(self.config.get('Window', 'left'))
        Window.top = int(self.config.get('Window', 'top'))

    def _set_window_size(self):
        width = int(self.config.get('Window', 'width'))
        height = int(self.config.get('Window', 'height'))
        Window.size = (width, height)

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20})
        config.setdefaults('Window', {
            'left': Window.left, 'top': Window.top,
            # 'width': Window.width, 'height': Window.height,
        })
        config.setdefaults('Pomodoro', {
            'pomodoro_duration': 25,
            'pomodoro_rest': 5
        })

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('My Label', self.config, data=mylable)
        settings.add_json_panel('Pomodoro', self.config, data=pomodoro)
        # settings.add_json_panel('Window', self.config, data=window)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "My Label":
            if key == "text":
                self.root.ids.label.text = value
            elif key == 'font_size':
                self.root.ids.label.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super().close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """

    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))
