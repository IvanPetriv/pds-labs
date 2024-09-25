from kivy.lang import Builder
from kivy.uix.widget import Widget


Builder.load_file('view/rc5_view.kv')


class Rc5Controller(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def encrypt_string(self):
        pass

    def decrypt_string(self):
        pass
