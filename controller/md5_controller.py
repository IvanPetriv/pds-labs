from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from plyer import filechooser

from model.md5_model import Md5


Builder.load_file('view/md5_view.kv')


class Md5Controller(Widget):
    """
    Widget that takes a string argument and converts it to its hash form
    using MD5 algorithm
    """
    normal_text: StringProperty | str = StringProperty("")
    hashed_text: StringProperty | str = StringProperty("")

    def open_file(self) -> None:
        """
        Opens the file manager that allows you to choose a text file,
        after that reads and stores the contents of the chosen file
        """
        path = filechooser.open_file(title="Pick a text file..", filters=["*.txt"])
        with open(path[0], "r") as text_file:
            self.normal_text = text_file.read()

    def save_to_file(self) -> None:
        """
        Opens the file manager that allows you to choose a directory,
        after that creates a file and stores the hash there
        """
        file_path = filechooser.save_file(title="Save Hash", filters=["*.txt"])

        if file_path:
            if isinstance(file_path, list):
                file_path = file_path[0]
            try:
                with open(file_path, 'w') as file:
                    file.write(self.hashed_text)
                print(f"File saved at: {file_path}")
            except IOError as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("Save operation cancelled.")


    def generate_hash(self) -> None:
        """
        Generates an MD5 hash from the input text and outputs it
        """
        result = Md5.md5(self.normal_text)
        self.hashed_text = result
