"""
Settings
==============

This file contains Tempo settings classes.
It allows the user to change app default settings and stores these changes.

When the user next runs the programs, their changes are restored.

"""

from os import path

from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.settings import SettingsWithSidebar, SettingsWithTabbedPanel
from kivy.utils import platform

debug = True

CURRENT_DIR = path.dirname(__file__)


if platform == 'win':
    # Disable multitouch on Windows.
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    # Disable app stop when ESC button pressed.
    Config.set('kivy', 'exit_on_escape', '0')


# DEFAULTS
D = {
    'POMODURATION': 25,
    'POMOREST': 5,
    'WORKTIME': 6,
    'WINDOW_WIDTH': 800,
    'WINDOW_HEIGHT': 600,
    'WINDOW_LEFT': 368,
    'WINDOW_TOP': 132,
    'SCREEN': 'taskscreen'
}


class ConfiguredApp(App):
    """This class is used to create settings for the app."""

    settings_cls = SettingsWithSidebar
    use_kivy_settings = True

    def configure_app(self):
        """Set all application configurations.

        Use this once when launch the application.
        """
        self.configure_window()
        self.set_screen()
        self.set_pomodoro_values()

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

    def build_config(self, config):
        """Set the default values for the configs sections."""
        # config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20})
        config.setdefaults('Window', {
            'left': D['WINDOW_LEFT'], 'top': D['WINDOW_TOP'],
            'width': D['WINDOW_WIDTH'], 'height': D['WINDOW_HEIGHT'],
        })
        config.setdefaults('General', {
            'pomodoro_duration': D['POMODURATION'],
            'pomodoro_rest': D['POMOREST'],
            'worktime': D['WORKTIME'],
            'defaultscreen': D['SCREEN'],
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
            if key == "worktime":
                if int(value) >= 23:
                    value = D['WORKTIME']
                    config.set('General', 'worktime', D['WORKTIME'])
                    config.write()
                # self.root.ids.label.text = value
            elif key == 'font_size':
                self.root.ids.label.font_size = float(value)
        if section == 'General':
            self.set_pomodoro_values()

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
