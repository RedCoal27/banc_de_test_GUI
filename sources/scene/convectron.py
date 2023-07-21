from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

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
        ratio = (0.14, 0.08)
        super().__init__(parent.translator, pos, ratio, "#E2F0D9")
        self.create_labels(key)
        

    def create_labels(self,key):
        """
        Creates labels for the Convectron widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key,alignment=Qt.AlignmentFlag.AlignTop)
        self.create_label("(convectron)")
        self.create_label("pressure", value = "RS485")