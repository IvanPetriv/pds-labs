from __future__ import annotations

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from model.md5_model import Md5
from model.rc5_model import RC5_CBC_PAD


Builder.load_file('view/rc5_view.kv')


class MyDropDown(BoxLayout):
    selected_option = ""

    def on_dropdown_select(self, text):
        self.selected_option = text


class Rc5Controller(Widget):
    word_size: NumericProperty = NumericProperty(0)
    round_count: NumericProperty = NumericProperty(0)
    key_size: NumericProperty = NumericProperty(0)
    result: StringProperty | str = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_properties(self):
        return (int(self.ids.input_word_size.text or 0),
                int(self.ids.input_round_count.text or 0),
                int(self.ids.input_key_size.text or 0))

    def encrypt_string(self):
        rc5 = RC5_CBC_PAD(*self.get_properties())
        passphrase = Md5.md5(self.ids.input_passphrase.text)
        encrypted_text = rc5.encrypt(self.ids.input_text.text, passphrase)
        self.result = encrypted_text

    def decrypt_string(self):
        rc5 = RC5_CBC_PAD(*self.get_properties())
        passphrase = Md5.md5(self.ids.input_passphrase.text)
        decrypted_text = rc5.decrypt(self.ids.input_text.text, passphrase)
        self.result = decrypted_text
