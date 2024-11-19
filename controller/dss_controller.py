from __future__ import annotations

from Crypto.PublicKey.DSA import DsaKey
from kivy.lang import Builder
from kivy.uix.widget import Widget

from model.dss_model import Dss
from services.file_manager import open_file, save_file


Builder.load_file('view/dss_view.kv')


class DssController(Widget):
    private_key_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\private_key.pem"
    public_key_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\public_key.pem"
    signature_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\signature.bin"
    decrypted_file_filename: str = r"D:\LPNU\University\4-year\1-term\PDS\code\output\decrypted_file.bin"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text: bytes | None = None
        self.signature: bytes | None = None

    def get_text(self):
        return self.text or bytes(self.ids.input_text.text, "utf-8")

    def get_signature(self):
        return self.signature or bytes.fromhex(self.ids.input_signature.text)

    def generate_key_pair(self):
        private_key, public_key = Dss.generate_key_pair()
        Dss.save_key_to_file(public_key, self.public_key_filename)
        Dss.save_key_to_file(private_key, self.private_key_filename, True)

    def sign_message(self):
        text: bytes = self.get_text()
        key: DsaKey = Dss.load_key_from_file(self.private_key_filename)
        signature = Dss.sign_message(text, key)
        self.ids.result_data.text = "Result is copied to signature input!"
        self.ids.input_signature.text = signature.hex()
        save_file(signature, self.signature_filename)

    def verify_message(self):
        text: bytes = self.get_text()
        signature: bytes = self.get_signature()
        key: DsaKey = Dss.load_key_from_file(self.public_key_filename)
        verification = Dss.verify_signature(text, signature, key)
        verification_str = f"The message {'IS' if verification else 'is NOT'} authentic"
        self.ids.result_data.text = str(verification_str)

    def open_text_file(self):
        self.text = open_file()
        self.ids.input_text.hint_text = "File is being used"

    def open_signature_file(self):
        self.signature = open_file()
        self.ids.input_signature.hint_text = "File is being used"
