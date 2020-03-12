from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class GridApp(App):
    def build(self):

        gl = GridLayout(rows=6, cols=4, padding=[30], spacing=3)
        gl.add_widget( Button(text='7' ) )
        gl.add_widget( Button(text='8' ) )
        gl.add_widget( Button(text='9' ) )
        gl.add_widget( Button(text='X' ) )
        
        gl.add_widget( Button(text='4' ) )
        gl.add_widget( Button(text='5' ) )
        gl.add_widget( Button(text='6' ) )
        gl.add_widget( Button(text='-' ) )

        gl.add_widget( Button(text='1' ) )
        gl.add_widget( Button(text='2' ) )
        gl.add_widget( Button(text='3' ) )
        gl.add_widget( Button(text='+' ) )

        gl.add_widget( Widget() )
        gl.add_widget( Button(text='0' ) )
        gl.add_widget( Button(text=',' ) )
        gl.add_widget( Button(text='=' ) )

        return gl

        
        for x in range(25):
            gl.add_widget(Button(text='Кнопка {}'.format(x+1)))
        
        return gl




if __name__ == "__main__":
    GridApp().run()
