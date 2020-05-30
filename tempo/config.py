# Disable multitouch on Windows
from kivy.utils import platform

debug = True

if platform == 'win':
    from kivy.config import Config
    from kivy.core.window import Window
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('kivy', 'exit_on_escape', '0')

    if debug is True:
        print(Window.left)
        print(Window.top)
        Window.left = 0
        Window.top = -800
