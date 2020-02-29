from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from pygments.lexers.html import HtmlLexer

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')


class MyApp(App):
    def build(self):
        s = Scatter()
        fl = FloatLayout(size = (300, 300))
        # return CodeInput(lexer = HtmlLexer())
        s.add_widget(fl)
        fl.add_widget(Button(text = 'Это моя первая кнопка!',
        font_size = 16,
        on_press = self.btn_press,
        background_color = [.31, .72, 1, 1],
        background_normal = '',
        size_hint = (.5, .25),
        pos = (640 / 4, 480 / 2 - (480 / 8))
        ))

        return s
        return fl
        return Button(text = 'Это моя первая кнопка!',
        font_size = 30,
        on_press = self.btn_press,
        background_color = [.31, .72, 1, 1],
        background_normal = ''
        )
    
    def btn_press(self, instance):
        print('Кнопка нажата! ')
        instance.text = 'Я нажата. '




if __name__ == "__main__":
    MyApp().run()
