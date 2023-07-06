from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class Chamber(CustomWidget):
    def __init__(self, translator, pos , parent=None):
        ratio = [0.4, 0.2]
        super().__init__(translator, pos, ratio, "#00B0F0", parent)
        self.create_label("chamber", alignment = Qt.AlignCenter)