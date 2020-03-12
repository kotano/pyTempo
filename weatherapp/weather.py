import json

from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior



class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        # search_template = (
        #     "https://samples.openweathermap.org/data/2.5/find"
        #     "?q={}&appid=b6907d289e10d714a6e88b30761fae22")
        search_template = (
            "https://api.openweathermap.org/data/2.5/find?"
            "q={}&typle=like&appid=906855b8517b3e04738c90ba861ef8fa"
            )
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
        self.search_results.data = [{'text': str(x)} for x in cities]
        print(f"self.search_results.data={self.search_results.data}")


class WeatherRoot(BoxLayout):
    pass


class TestApp(App):
    title = "Weather App"

    def build(self):
        return Builder.load_file("weather.kv")


if __name__ == '__main__':
    TestApp().run()