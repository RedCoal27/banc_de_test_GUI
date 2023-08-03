from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class IonGauge(CustomWidget):
    def __init__(self, pos , key , parent):
        """
        Initializes a Convectron widget.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - parent: a parent widget (optional)
        """
        ratio = (0.12, 0.10)
        super().__init__(parent.translator, pos, ratio, "#E2F0D9")
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the Convectron widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.create_label("command", value = "off")
        self.create_label("reading", value = "off")
        self.create_label("pressure", value = "RS485")