from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from window.pirani_config_gui import PiraniConfigGui
from internal.constant import PiraniConfig


class JaugePression(CustomWidget):
    def __init__(self, pos , key , parent):
        """
        Initializes a JaugePression widget.

        Args:
        translator: a translator object used for internationalization
        pos: a tuple representing the position of the widget
        key: a string representing the key of the widget
        parent: a parent widget (optional)
        """
        self.pirani_config_gui = None
        self.parent = parent
        self.key = key
        self.value = 1000
        ratio = (0.12, 0.12)
        super().__init__(parent.translator, pos, ratio, "#E2F0D9")
        self.create_labels(key)
        self.create_button("pirani_config", self.open_pirani_config)
        

    def create_labels(self,key):
        """
        Creates labels for the JaugePression widget.

        Args:
        key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.create_label("gas_type", gas_type = "")
        self.create_label("pressure", value = "0", unit = "")

    def update_pressure(self, value):
        if value[0] == 'error':
            self.update_label('pressure', value = "error", unit = "")
            return

        unit = (int(value[1], 16) >> 4) & 3 #permet de récuperer uniquement les 2 bit indiquant l'unité
        gas_index = (int(value[1], 16) >> 12) & 7 #permet de récuperer uniquement les 2 bit indiquant le gas enregistré
        self.update_label("gas_type", gas_type = PiraniConfig.gas_types[gas_index])
        pressure = float(value[0])
        if pressure < 0.1:
            pressure_str = f"{pressure:.2e}"  # Utilise l'écriture scientifique avec 1 chiffre après le point
            base, exp = pressure_str.split("e")  # Split la chaîne en base et exposant
            # Enlève le zéro si l'exposant est de deux chiffres (par exemple, -02 devient -2)
            if len(exp) == 3:
                exp = exp[0] + exp[2]
            pressure = base + "E" + exp
        else:
            pressure = f"{pressure:.3f}"
        self.value = pressure
        pressure += " "

        self.update_label('pressure', value = pressure, unit = PiraniConfig.units_types[unit - 1])
        if self.pirani_config_gui is not None and self.pirani_config_gui.isVisible():
            self.pirani_config_gui.update_status_bits(int(value[1], 16))

    def open_pirani_config(self):
        if self.parent.serial_reader.ser is not None:
            self.pirani_config_gui = PiraniConfigGui(self.parent,self.key)
            self.pirani_config_gui.show()


    def get_value(self):
        """
        Returns the value of the label.
        """
        value = self.value
        #convert unit to torr
        if value == "overrange":
            return 1000
        if self.parent.config[self.key]["pressure_unit"] == "mBar":
            value = float(value)*0.75
        elif self.parent.config[self.key]["pressure_unit"] == "Pascal":
            value = float(value)*0.0075
        return float(value)

