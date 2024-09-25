from kivy.lang import Builder
from kivy.uix.widget import Widget

# DO NOT DELETE THIS
from controller.lcg_controller import LcgController
from controller.md5_controller import Md5Controller
from controller.rc5_controller import Rc5Controller
from controller.rsa_controller import RsaController
from controller.dss_controller import DssController


Builder.load_file('view/base_view.kv')


class BaseController(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
