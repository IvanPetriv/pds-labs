from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

from model.md5_model import Md5
from services import file_manager


Builder.load_file('view/md5_view.kv')


class Md5Controller(Widget):
    """
    Widget that takes a string argument and converts it to its hash form
    using MD5 algorithm.
    """
    normal_text: StringProperty | str = StringProperty("")
    hashed_text: StringProperty | str = StringProperty("")

    def open_file(self) -> None:
        """
        Opens the file manager to choose a text file, reads the content,
        and stores it in `normal_text`.
        """
        data = file_manager.open_file()

        if data is not None:
            self.normal_text = data


    def save_to_file(self) -> None:
        """
        Opens the file manager to choose a directory and saves the MD5 hash
        to a file.
        """
        file_manager.save_file(self.hashed_text)


    def generate_hash(self) -> None:
        """
        Generates an MD5 hash from `normal_text` and stores it in `hashed_text`.
        """
        self.normal_text = self.ids.input_text.text
        result = Md5.md5(self.normal_text)
        self.hashed_text = result

    def check_file(self) -> None:
        """
        Checks if the hash of the chosen file matches `normal_text`.
        """
        file_data = file_manager.open_file()

        if file_data is None:
            return

        hashed_data = Md5.md5(file_data)
        if hashed_data == self.normal_text:
            self.hashed_text = "File is valid."
        else:
            self.hashed_text = "File is not valid."
