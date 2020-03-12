from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

class AnchorApp(App):
    def build(self):
        al = AnchorLayout()
        bl = BoxLayout(orientation='vertical', size_hint=[None, None], size=[300, 200])
        
        bl.add_widget( TextInput())
        bl.add_widget( TextInput())
        bl.add_widget(Button(text='Войти'))
        
        al.add_widget(bl)
        return al


if __name__ == "__main__":
    AnchorApp().run()