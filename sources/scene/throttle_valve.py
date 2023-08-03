from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class ThrottleValve(CustomWidget):
    def __init__(self, pos , key, parent):
        """
        Initializes a ThrottleValve object.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - number: a string representing the number of the widget (optional)
        - parent: a parent widget (optional)
        """
        ratio = (0.11, 0.25)
        super().__init__(parent.translator, pos, ratio, "#F8CBAD")
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self,key):
        """
        Creates labels for the ThrottleValve widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("open", state = "false")
        self.create_label("close", state = "false")
        self.create_label("steps", state = "false")
        self.create_label("hysteresis", state = "")
        self.create_label("cmd", state = "false")


    def create_buttons(self):
        """
        Creates buttons for the ThrottleValve widget.
        """
        self.create_button("cycle")
