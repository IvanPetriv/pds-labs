from __future__ import annotations

import time

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from model.md5_model import Md5
from model.rc5_model import RC5_CBC_PAD
from services import file_manager


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
    text: bytes = bytes()
    result_text: bytes = bytes()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_properties(self):
        return (int(self.ids.input_word_size.text or 0),
                int(self.ids.input_round_count.text or 0),
                int(self.ids.input_key_size.text or 0))

    def generate_hash(self, key: str, key_len: int) -> str:
        hashed_key: str = Md5.md5(self.ids.input_passphrase.text)
        if key_len > 64:
            hashed_key += Md5.md5(hashed_key)
            hashed_key: bytes = bytes.fromhex(hashed_key)[:key_len]
        else:
            hashed_key: bytes = bytes.fromhex(hashed_key)[:key_len]
        return hashed_key.hex()

    def open_file(self):
        data = file_manager.open_file()

        if data is not None:
            self.text = data

    def encrypt_string(self):
        if len(self.text):
            text: bytes = self.text
        else:
            text: str = self.ids.input_text.text

        rc5 = RC5_CBC_PAD(*self.get_properties())
        passphrase = self.generate_hash(self.ids.input_passphrase.text, self.get_properties()[2])
        start_time = time.time_ns()
        encrypted_text = rc5.encrypt(text, passphrase)
        print(f"Encryption time: {round((time.time_ns()-start_time)/10**6, 3)}ms for {len(text)}-byte text")
        self.result = encrypted_text
        file_manager.save_file(bytes(encrypted_text, "utf-8"), "encrypted.bin")

    def decrypt_string(self):
        rc5 = RC5_CBC_PAD(*self.get_properties())
        passphrase = self.generate_hash(self.ids.input_passphrase.text, self.get_properties()[2])
        start_time = time.time_ns()
        if len(self.text):
            decrypted_text: bytes = rc5.decrypt(self.text, passphrase)
        else:
            decrypted_text = rc5.decrypt(self.ids.input_text.text, passphrase)
        print(f"Decryption time: {round((time.time_ns()-start_time)/10**6, 3)}ms for {len(decrypted_text)}-byte text")
        self.result = decrypted_text.decode("utf-8")
        file_manager.save_file(decrypted_text, "decrypted.bin")
