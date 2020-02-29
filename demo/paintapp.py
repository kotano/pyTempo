from kivy.app import App
from kivy.uix.widget import Widget

from kivy.graphics import (Color, Ellipse, Rectangle, Line)


class PainterWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(0, 1, 0, 1)
            Rectangle(pos = (100, 100), size = (50, 50) )


class PaintApp(App):
    def build(self):
        return PainterWidget()



if __name__ == "__main__":
    PaintApp().run()
