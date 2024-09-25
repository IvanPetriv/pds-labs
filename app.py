from kivy.app import App

from controller.base_controller import BaseController


class BaseApp(App):
    """
    Class that manages the GUI
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return BaseController()
