from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class Interlock(CustomWidget):
    def __init__(self, translator, pos , key , parent=None):
        ratio = (0.15, 0.15)
        super().__init__(translator, pos, ratio, "#FFD966", parent)
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("")
        self.create_label("Rouphing pump OFF")
        self.create_label("Pump Pressure >100mT")
        self.create_label("Chamber OPEN")
        self.create_label("Chamber Pressure >100mT")
        self.create_label("")

