from __future__ import annotations

import time

from Crypto.PublicKey.RSA import RsaKey
from kivy.lang import Builder
from kivy.uix.widget import Widget

from model.rsa_model import Rsa
from services.file_manager import open_file, save_file


Builder.load_file('view/rsa_view.kv')


class RsaController(Widget):
    private_key_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\private_key.pem"
    public_key_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\public_key.pem"
    encrypted_file_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\encrypted_file.bin"
    decrypted_file_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\decrypted_file.bin"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text: bytes | None = None

    def encrypt(self):
        text: bytes = self.text or bytes(self.ids.input_text.text, "utf-8")
        key: RsaKey = Rsa.load_key_from_file(self.public_key_filename)
        start_time = time.time_ns()
        encrypted_text = Rsa.encrypt(text, key)
        print(f"Encryption time: {round((time.time_ns()-start_time)/10**6, 3)}ms for {len(text)}-byte text")
        if not self.text:
            self.ids.result_data.text = encrypted_text.hex()
        else:
            save_file(encrypted_text, self.encrypted_file_filename)

    def decrypt(self):
        text: bytes = self.text or bytes(self.ids.input_text.text, "utf-8")
        key: RsaKey = Rsa.load_key_from_file(self.private_key_filename)
        start_time = time.time_ns()
        decrypted_text = Rsa.decrypt(text, key)
        print(f"Decryption time: {round((time.time_ns()-start_time)/10**6, 3)}ms for {len(decrypted_text)}-byte text")
        if not self.text:
            self.ids.result_data.text = decrypted_text.decode("utf-8")
        else:
            save_file(decrypted_text, self.decrypted_file_filename)

    def generate_key_pair(self):
        public_key, private_key = Rsa.generate_key_pair(8_192)
        Rsa.save_key_to_file(public_key, self.public_key_filename)
        Rsa.save_key_to_file(public_key, self.private_key_filename, True)

    def open_text_file(self):
        self.text = open_file()
        self.ids.input_text.hint_text = "File is being used"
