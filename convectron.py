from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class Convectron(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        """
        Initializes a Convectron widget.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - parent: a parent widget (optional)
        """
        ratio = [0.14, 0.08]
        super().__init__(translator, pos, ratio, "#E2F0D9", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the Convectron widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignTop)
        self.create_label("(convectron)")
        self.create_label("pressure", value = "RS485")


    # def update_DI(self, up, down):
    #     """
    #     Updates the DI labels of the Convectron widget.

    #     Args:
    #     - up: a boolean representing the state of the up DI
    #     - down: a boolean representing the state of the down DI
    #     """
    #     self.update_label('di_up', state = "false" if up else "true")
    #     self.update_label('di_down', state = "false" if down else "true")
    #     self.update_label('position', state = "unknown" if up*2 == down else "up" if up else "down")