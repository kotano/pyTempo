from kivy.app import App
from kivy.config import Config
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.data = [{'text': str(values)}
        #              for values in ['Palo Alto, MX', 'Palo Alto, US']]


class WeatherRoot(BoxLayout):
    pass


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_result = ObjectProperty()

    def search_location(self):
        search_template = (
            'http://api.openweathermap.org/data/2.5/find'
            '?q={}&type=like&appid=906855b8517b3e04738c90ba861ef8fa'
        )
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        cities = [{'text':'{} ({})'.format(d['name'], d['sys']['country'])}
                  for d in data['list']]
        self.search_results.data = cities


class TempoApp(App):
    pass
    # def build(self):
    #     bl = ( BoxLayout() )
    #     gl = ( GridLayout() )

    #     gl.add_widget(Label(text='Hello!'))
    #     bl.add_widget( gl )

    # return bl


if __name__ == "__main__":
    TempoApp().run()
