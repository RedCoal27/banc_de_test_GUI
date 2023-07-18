from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class MotorisedLift(CustomWidget):
    def __init__(self, translator, pos , key , number= "" , parent=None):
        """
        Constructor for the MotorisedLift class.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - number: a string representing the number of the widget (optional)
        - parent: a parent widget (optional)
        """
        ratio = [0.101, 0.18]
        super().__init__(translator, pos, ratio, "#F8CBAD", parent)
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self,key):
        """
        Creates labels for the MotorisedLift widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("p_home", state = "false")
        self.create_label("p_prcs", state = "false")
        self.create_label("steps", state = "false")
        self.create_label("cmd", state = "")


    def create_buttons(self):
        """
        Creates buttons for the MotorisedLift widget.
        """
        self.create_button("cycle")

    # def update_DI(self, up, down):
    #     """
    #     Updates the DI labels of the MotorisedLift widget.

    #     Args:
    #     - up: a boolean representing the state of the up DI
    #     - down: a boolean representing the state of the down DI
    #     """
    #     self.update_label('di_up', state = "false" if up else "true")
    #     self.update_label('di_down', state = "false" if down else "true")
    #     self.update_label('position', state = "unknown" if up*2 == down else "up" if not up else "down")