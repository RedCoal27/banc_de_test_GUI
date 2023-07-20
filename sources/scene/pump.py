from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class Pump(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = (0.1, 0.15)
        super().__init__(translator, pos, ratio, "#4472C4", parent)
        self.create_labels(key)
        self.create_button("change_state")
        

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
