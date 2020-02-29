from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# Config.set()


class TempoApp(App):
    def build(self):
        bl = ( BoxLayout() ) 
        gl = ( GridLayout() )

        gl.add_widget(Label(text='Hello!'))
        bl.add_widget( gl )


        return bl

if __name__ == "__main__":
    TempoApp().run()
