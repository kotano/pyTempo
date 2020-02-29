from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.anchorlayout import AnchorLayout

class AnchorApp(App):
    def build(self):
        al = AnchorLayout(anchor_x='left', anchor_y='top')
        
        for x in range(1):
            al.add_widget(Button(text='Кнопка {}'.format(x+1), size_hint=[.5, .5]))
        
        return al


if __name__ == "__main__":
    AnchorApp().run()