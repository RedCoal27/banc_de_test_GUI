from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class RoughingPump(CustomWidget):
    def __init__(self, pos , key , parent):
        ratio = (0.1, 0.12)
        super().__init__(parent.translator, pos, ratio, "#4472C4")
        self.create_labels(key)
        self.create_button("change_state")
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("cmd", state = "false")
        self.create_label("status", state = "false")
        self.create_label("Error", state = "false")
