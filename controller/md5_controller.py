from kivy.lang import Builder
from kivy.uix.widget import Widget
from plyer import filechooser

from model.md5_model import Md5


Builder.load_file('view/md5_view.kv')


class Md5Controller(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def open_file(self):
        path = filechooser.open_file(title="Pick a text file..", filters=["*.txt"])
        print(path)
        with open(path[0], "r") as text_file:
            self.ids.input_text.text = text_file.read()


    def generate_hash(self):
        print(self.ids.input_text.text, self.ids.input_text)
        result = Md5.md5(self.ids.input_text.text)
        print(result)
        self.ids.result_data.text = result
