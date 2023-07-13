from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class Pump(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = [0.1, 0.1]
        super().__init__(translator, pos, ratio, "#4472C4", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("cmd", state = "false")
        self.create_label("status", state = "false")
        self.create_label("accelerate", state = "false")


    # def update_DI(self, up, down):
    #     """
    #     Updates the DI labels of the FourWay widget.

    #     Args:
    #     - up: a boolean representing the state of the up DI
    #     - down: a boolean representing the state of the down DI
    #     """
    #     self.update_label('di_up', state = "false" if up else "true")
    #     self.update_label('di_down', state = "false" if down else "true")
    #     self.update_label('position', state = "unknown" if up*2 == down else "up" if up else "down")