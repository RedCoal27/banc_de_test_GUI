from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget
from pirani_config_gui import PiraniConfigGui
from internal.constant import PiraniConfig


class Convectron(CustomWidget):
    def __init__(self, pos , key , parent):
        """
        Initializes a Convectron widget.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - parent: a parent widget (optional)
        """
        self.pirani_config_gui = None
        self.parent = parent
        self.key = key
        ratio = (0.12, 0.12)
        super().__init__(parent.translator, pos, ratio, "#E2F0D9")
        self.create_labels(key)
        self.create_button("pirani_config", self.open_pirani_config)
        

    def create_labels(self,key):
        """
        Creates labels for the Convectron widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.create_label("gas_type", gas_type = "")
        self.create_label("pressure", value = "0", unit = "")

    def update_pressure(self, value):
        unit = (int(value[1], 16) >> 4) & 3 #permet de récuperer uniquement les 2 bit indiquant l'unité
        gas_index = (int(value[1], 16) >> 12) & 7 #permet de récuperer uniquement les 2 bit indiquant le gas enregistré
        self.update_label("gas_type", gas_type = PiraniConfig.gas_types[gas_index])
        self.update_label('pressure', value = float(value[0]), unit = PiraniConfig.units_types[unit - 1])
        if self.pirani_config_gui is not None and self.pirani_config_gui.isVisible():
            self.pirani_config_gui.update_status_bits(int(value[1], 16))

    def open_pirani_config(self):
        if self.parent.serial_reader.ser is not None:
            self.pirani_config_gui = PiraniConfigGui(self.parent,self.key)
            self.pirani_config_gui.show()


