from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from internal.logger import Logger


class Baratron(CustomWidget):
    def __init__(self, pos , key , parent):
        ratio = (0.08, 0.1)
        self.offset = 0
        self.key = key
        super().__init__(parent.translator, pos, ratio, "#C5E0B4")
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("pressure", value = "0", unit= "mBar")
        self.create_label_with_spin_box("offset", unit="mbar", initial_value=0, min_value = -100, max_value=100, function=self.update_offset)
        self.create_label("size", value = "0", unit="mbar")

    def update_AI(self, value):
        """
        Updates the value of the label.
        """
        value = float(value) - self.offset
        self.update_label("pressure", value = value)

    def update_offset(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()





