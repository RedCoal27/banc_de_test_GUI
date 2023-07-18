from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class FourWay(CustomWidget):
    def __init__(self, translator, pos , key , number= "" , parent=None):
        """
        Initializes a FourWay object.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - number: a string representing the number of the widget (optional)
        - parent: a parent widget (optional)
        """
        ratio = [0.101, 0.18]
        self.FourWay_number = number
        super().__init__(translator, pos, ratio, "#FBE5D6", parent)
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, number = self.FourWay_number,alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("do_up", state = "false")
        self.create_label("do_down", state = "false")
        self.create_label("di_up", state = "false")
        self.create_label("di_down", state = "false")
        self.create_label("position", state = "unknown")


    def create_buttons(self):
        """
        Creates buttons for the FourWay widget.
        """
        self.create_button("cycle", self.open_windows)

    def update_DI(self, up, down):
        """
        Updates the DI labels of the FourWay widget.

        Args:
        - up: a boolean representing the state of the up DI
        - down: a boolean representing the state of the down DI
        """
        self.update_label('di_up', state = "false" if up else "true")
        self.update_label('di_down', state = "false" if down else "true")
        self.update_label('position', state = "unknown" if up*2 == down else "up" if not up else "down")