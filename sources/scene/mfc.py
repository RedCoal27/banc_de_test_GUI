from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from internal.logger import Logger

class MFC(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = (0.1, 0.12)
        self.offset = 0
        super().__init__(translator, pos, ratio, "#B4C7E7", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_spin_box("setpoint", initial_value=0, units="sccm", function=self.update_AO)
        self.create_label("actual", value = "0")
        self.create_label_with_spin_box("offset", initial_value=0, units="sccm", min_value = -100, max_value=100, function=self.update_offset)
        self.create_label_with_spin_box("size", initial_value=1000, units="sccm", function=self.update_size)



    def update_AI(self, value):
        """
        Updates the value of the label.
        """
        value = float(value) + self.offset
        print(value)
        self.update_label("actual", value = value)

    def update_AO(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"AO changed to {spin_box.value()}")
        print(spin_box.value())

    def update_offset(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"Offset changed to {spin_box.value()}")
        self.offset = spin_box.value()

    def update_size(self, spin_box):
        """
        Change the upper limit of the spin box to the value of the spin box.
        """
        Logger.debug(f"Size changed to {spin_box.value()}")
        self.update_spin_box("setpoint", spin_box.value())
