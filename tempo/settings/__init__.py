"""
Settings
==============

This file contains Tempo settings classes.
It allows the user to change app default settings and stores these changes.

When the user next runs the programs, their changes are restored.

"""

from os import path
from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.settings import SettingsWithSidebar, SettingsWithTabbedPanel
from kivy.utils import platform
from kivy.properties import DictProperty, ConfigParserProperty
from kivy.lang.builder import Builder

# CURRENT_DIR = path.dirname(__file__)
CURRENT_DIR = Path(__file__).parent


if platform == 'win':
    # Disable multitouch on Windows.
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    # Disable app stop when ESC button pressed.
    Config.set('kivy', 'exit_on_escape', '0')

# DEFAULTS
D = {
    'POMODURATION': 50,
    'POMOREST': 10,
    'WORKTIME': 6,
    'WINDOW_WIDTH': 800,
    'WINDOW_HEIGHT': 600,
    'WINDOW_LEFT': 368,
    'WINDOW_TOP': 132,
    'SCREEN': 'taskscreen',
    'COLOR_SCHEME': 'TempoBlue'
}

# COLORS
C = {
    'TempoBlue': {
        'background': [1, 1, 1, 1],
        'button': [.89, .91, .96, 1],
        'accent': [.67, .79, .96, 1],
        'active': [1, .78, .33, 1],
        'text_dark': [0, 0, 0, 1],
        'text_bright': [1, 1, 1, 1]
    },
    'TempoBright': {
        'background': [1, 1, 1, 1],
        'button': [.89, .91, .96, 1],
        'accent': [1, .78, .33, 1],
        'active': [.92, .34, .34, 1],
        'text_dark': [0, 0, 0, 1],
        'text_bright': [1, 1, 1, 1]
    },
    # OLD
    'Aquamarine': {
        'background': [1, 1, 1, 1],
        'accent': [.70, .88, .87, .9],
        'text_dark': [0, 0, 0, 1],
        'text_bright': [1, 1, 1, 1]
    }
}


class ConfiguredApp(App):
    """This class is used to create settings for the app."""
    use_kivy_settings = True
    settings_cls = SettingsWithSidebar

    ROOT_DIR = CURRENT_DIR.parent.parent
    ICONS_DIR = ROOT_DIR / 'data' / 'icons'
    WIDGETS_DIR = ROOT_DIR / 'tempo' / 'widgets'
    COLORS = C

    icon = str(ICONS_DIR / 'icon_white.png')
    colors = DictProperty()
    # color_scheme = ConfigParserProperty(
    #     'TempoBlue', 'General', 'color_scheme', 'kivy')

    def build_config(self, config):
        """Set the default values for the configs sections."""
        # config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20})
        config.setdefaults('General', {
            'pomodoro_duration': D['POMODURATION'],
            'pomodoro_rest': D['POMOREST'],
            'worktime': D['WORKTIME'],
            'defaultscreen': D['SCREEN'],
            'color_scheme': D['COLOR_SCHEME']
        })
        config.setdefaults('Window', {
            'left': D['WINDOW_LEFT'], 'top': D['WINDOW_TOP'],
            'width': D['WINDOW_WIDTH'], 'height': D['WINDOW_HEIGHT'],
        })

    def build_settings(self, settings):
        """Add our custom section to the default configuration object."""
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        # settings.add_json_panel(
        #     'My Label', self.config, './tempo/settings.json')
        settings.add_json_panel(
            'General', self.config, path.join(CURRENT_DIR, 'general.json'))
        settings.add_json_panel(
            'Window', self.config, path.join(CURRENT_DIR, 'window.json'))

    def on_config_change(self, config, section, key, value):
        """Respond to changes in the configuration."""
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "General":
            self.set_pomodoro_values()
            if key == "worktime":
                if int(value) >= 23:
                    value = D['WORKTIME']
                    config.set('General', 'worktime', D['WORKTIME'])
                    config.write()
                # self.root.ids.label.text = value
            elif key == 'color_scheme':
                self.on_color_scheme()
            # elif key == 'font_size':
            #     self.root.ids.label.font_size = float(value)
            # elif key == 'font_size':
            #     self.root.ids.label.font_size = float(value)

    def configure_app(self):
        """Set all application configurations.

        Use this once when launch the application.
        """
        Builder.load_file(str(self.WIDGETS_DIR / 'task.kv'))
        self.on_color_scheme()
        self.configure_window()
        self.set_screen()
        self.set_pomodoro_values()

    def on_color_scheme(self):
        print(self.colors)
        self.colors = C[self.config.get('General', 'color_scheme')]
        print(self.colors)
        # self.colors = C[self.color_scheme]
        # self.colors = COLORS[self.config.get('General', 'color_scheme')]

    def get_application_config(self):
        """Set app config file location to user_data_dir."""
        filepath = path.join(self.user_data_dir, '%(appname)s.ini')
        return super().get_application_config(filepath)

    def configure_window(self):
        """Set window size and position depepending on config values."""
        if platform in ['ios', 'android']:
            return
        Window.bind(on_request_close=self.remember_window)
        self._set_window_size()
        self._set_window_pos()

    def set_screen(self):
        self.defaultscreen = self.config.get('General', 'defaultscreen')
        pass

    def _set_window_pos(self):
        Window.left = int(self.config.get('Window', 'left'))
        Window.top = int(self.config.get('Window', 'top'))

    def _set_window_size(self):
        width = int(self.config.get('Window', 'width'))
        height = int(self.config.get('Window', 'height'))
        Window.size = (width, height)

    def set_pomodoro_values(self):
        """Assign pomodoro values as an instance attributes."""
        self.pomoduration = int(self.config.get(
            'General', 'pomodoro_duration'))
        self.pomorest = int(self.config.get('General', 'pomodoro_rest'))
        self.worktime = int(self.config.get('General', 'worktime'))

    def close_settings(self, settings=None):
        """The settings panel has been closed."""
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super().close_settings(settings)

    def remember_window(self, *args):
        """Remember app window position and save to config."""
        self.config.set('Window', 'left', Window.left)
        self.config.set('Window', 'top', Window.top)
        self.config.set('Window', 'width', Window.width)
        self.config.set('Window', 'height', Window.height)
        self.config.write()


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """Custom settings pannel."""
    # It is not usually necessary to create subclass of a settings panel.
    # There are many built-in types that you can use out of the box
    # (SettingsWithSidebar, SettingsWithSpinner etc.).

    # You would only want to create a Settings subclass like this if
    # you want to change the behavior or appearance of
    # an existing Settings class.

    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))
