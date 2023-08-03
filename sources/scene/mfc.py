from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from internal.logger import Logger

from internal.config import Config

class MFC(CustomWidget):
    def __init__(self, pos, cmd, key , parent):
        ratio = (0.1, 0.12)
        self.offset = 0
        self.key = key
        self.cmd = cmd
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#B4C7E7")
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_spin_box("setpoint", initial_value=0, unit="sccm", function=self.update_AO)
        self.create_label("actual", value = "0")
        self.create_label_with_spin_box("offset", unit="sccm", initial_value=0, min_value = -100, max_value=100, function=self.update_offset)
        self.create_label("size", value = self.parent.config.get_constant_value(key), unit="sccm")


    def update_AI(self, value):
        """
        Updates the value of the label.
        """
        value = (float(value)/5*1000)
        value = int(round(value - self.offset))
        self.update_label("actual", value = value)

    def update_AO(self, spin_box):
        """
        Updates the value of the label.
        """

        self.parent.serial_reader.send_data(self.cmd, spin_box.value()/1000*5)  
        Logger.debug(f"{self.key} setpoint changed to {spin_box.value()}")

    def update_offset(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()

    # def update_size(self, spin_box):
    #     """
    #     Change the upper limit of the spin box to the value of the spin box.
    #     """
    #     Logger.debug(f"{self.key} size changed to {spin_box.value()}")
    #     self.update_spin_box("setpoint", spin_box.value())
