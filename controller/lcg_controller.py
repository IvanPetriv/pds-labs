from collections.abc import Callable

from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder

from model import lcg_model


Builder.load_file('view/lcg_view.kv')


class LabelledTextInput(BoxLayout):
    """
    Text input class which consists of descriptive label and standard text input.
    It has a filter which accepts digits, +, -, *, /, (, ).
    It can also be validated under certain conditions.
    """
    label_text: StringProperty | str = StringProperty("")  # Text of descriptive part
    hint_text: StringProperty | str = StringProperty("")  # Hint text of input
    is_valid: BooleanProperty | bool = BooleanProperty(True)  # Whether the value in input passed the validation
    input_validator: ObjectProperty | Callable | None = ObjectProperty(None)  # Function to validate input

    @staticmethod
    def expr_filter(input_str: str, from_undo):
        """
        Filters the input string so only allowed characters stay
        """
        allowed_chars = "0123456789+-*/()"
        return ''.join([char for char in input_str if char in allowed_chars])


class LcgController(Widget):
    """
    Widget that takes integers as arguments and shows the random sequence
    based on them with LCG algorithm
    """
    is_modulus_valid: BooleanProperty | bool = BooleanProperty(False)
    is_multiplier_valid: BooleanProperty | bool = BooleanProperty(False)
    is_increment_valid: BooleanProperty | bool = BooleanProperty(False)
    is_start_val_valid: BooleanProperty | bool = BooleanProperty(False)

    def check_modulus(self, value: str) -> None:
        """
        Checks if the value of input for modulus ``m`` is correct
        :param value: Value to check
        """
        try:
            self.is_modulus_valid = eval(value) > 0
        except (SyntaxError, ValueError):
            self.is_modulus_valid = False

        self.check_multiplier(self.ids.input_multiplier.text)
        self.check_increment(self.ids.input_increment.text)
        self.check_start_val(self.ids.input_start_val.text)

    def check_multiplier(self, value: str) -> None:
        """
        Checks if the value of input for multiplier ``a`` is correct
        :param value: Value to check
        """
        try:
            modulus: int = eval(self.ids.input_modulus.text)
            self.is_multiplier_valid = 0 <= eval(value) < modulus
        except (SyntaxError, ValueError):
            self.is_multiplier_valid = False

    def check_increment(self, value: str) -> None:
        """
        Checks if the value of input for increment ``c`` is correct
        :param value: Value to check
        """
        try:
            modulus: int = eval(self.ids.input_modulus.text)
            self.is_increment_valid = 0 <= eval(value) < modulus
        except (SyntaxError, ValueError):
            self.is_increment_valid = False

    def check_start_val(self, value: str) -> None:
        """
        Checks if the value of input for start value ``X0`` is correct
        :param value: Value to check
        """
        try:
            modulus: int = eval(self.ids.input_modulus.text)
            self.is_start_val_valid = 0 <= eval(value) < modulus
        except (SyntaxError, ValueError):
            self.is_start_val_valid = False

    def generate_sequence(self) -> None:
        """
        Generates random sequence with ``Count`` elements using ``m``, ``a``, ``c``, ``X0``
        :return:
        """
        # Retrieves data from inputs
        modulus: int = eval(self.ids.input_modulus.text)
        multiplier: int = eval(self.ids.input_multiplier.text)
        increment: int = eval(self.ids.input_increment.text)
        start_val: int = eval(self.ids.input_start_val.text)
        iterations: int = 1000 if self.ids.input_count.text == "" else eval(self.ids.input_count.text)

        # Checks if all values are correct
        if not all([self.is_modulus_valid, self.is_multiplier_valid,
                    self.is_increment_valid, self.is_start_val_valid]):
            raise ValueError

        # Generates the sequence and its period
        result: list[int] = lcg_model.generate_sequence(modulus, multiplier, increment, start_val, iterations)
        self.ids.result_list.data = [{"text": str(r)} for r in result]
        period: int = lcg_model.measure_period(result)
        self.ids.result_label.text = f"The sequence has the period: {period if period != -1 else 'full'}"

        # Writes data to file
        with open("output/sequence.txt", "w") as file:
            file.write("\n".join([str(r) for r in result]))
