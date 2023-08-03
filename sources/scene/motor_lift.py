from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class MotorisedLift(CustomWidget):
    def __init__(self, pos , key , parent):
        """
        Constructor for the MotorisedLift class.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - number: a string representing the number of the widget (optional)
        - parent: a parent widget (optional)
        """
        ratio = (0.101, 0.18)
        super().__init__(parent.translator, pos, ratio, "#F8CBAD")
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self,key):
        """
        Creates labels for the MotorisedLift widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("p_home", state = "false")
        self.create_label("p_prcs", state = "false")
        self.create_label("steps", state = "false")
        self.create_label("cmd", state = "")


    def create_buttons(self):
        """
        Creates buttons for the MotorisedLift widget.
        """
        self.create_button("cycle")
