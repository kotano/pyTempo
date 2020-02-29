from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class BoxApp(App):
    def build(self):
        # bl = BoxLayout(orientation='vertical', padding=[50, 10], spacing=100)
        bl = BoxLayout(orientation='vertical', padding=[150])
        bl.add_widget(TextInput())
        bl.add_widget(TextInput())
        bl.add_widget(Button(text='Войти'))
        return bl


if __name__ == "__main__":
    BoxApp().run()
