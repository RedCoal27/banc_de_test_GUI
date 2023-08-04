from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from internal.logger import Logger


class Baratron(CustomWidget):
    def __init__(self, pos , key , parent):
        ratio = (0.12, 0.1)
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
        self.create_label("pressure", value = "0", unit= " Torr")
        self.create_label_with_spin_box("offset", unit=" Torr", initial_value=0, min_value = -100, max_value=100, function=self.update_offset)
        self.create_label("size", value = "0.1", unit=" Torr")

    def update_AI(self, value):
        """
        Updates the value of the label.
        """
        unit = " Torr"
        value = float(value)
        if value > 10: 
            value = "overrange"
            unit = ""
        else :
            value = value*0.1/10 - self.offset
            value = f"{value:.2e}"  # Utilise l'écriture scientifique avec 1 chiffre après le point
            base, exp = value.split("e")  # Split la chaîne en base et exposant
            # Enlève le zéro si l'exposant est de deux chiffres (par exemple, -02 devient -2)
            if len(exp) == 3:
                exp = exp[0] + exp[2]
            value = base + "E" + exp
        self.update_label("pressure", value = value,unit = unit)

    def update_offset(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()





