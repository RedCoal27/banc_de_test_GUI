from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class Baratron(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = (0.14, 0.1)
        super().__init__(translator, pos, ratio, "#C5E0B4", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("pressure", value = "0")
        self.create_label("offset", value = "0")
        self.create_label("size", value = "0")

