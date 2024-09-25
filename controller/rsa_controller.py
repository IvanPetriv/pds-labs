from kivy.lang import Builder
from kivy.uix.widget import Widget


Builder.load_file('view/rsa_view.kv')


class RsaController(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
