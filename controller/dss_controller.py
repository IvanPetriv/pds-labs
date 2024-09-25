from kivy.lang import Builder
from kivy.uix.widget import Widget


Builder.load_file('view/dss_view.kv')


class DssController(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
