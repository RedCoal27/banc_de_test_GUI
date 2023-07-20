from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class MFC(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = (0.1, 0.12)
        super().__init__(translator, pos, ratio, "#B4C7E7", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("setpoint", value = "0")
        self.create_label("actual", value = "0")
        self.create_label("offset", value = "0")
        self.create_label("size", value = "0")

    def update_AI(self, value):
        """
        Updates the value of the label.
        """
        self.update_label("actual", value = value)