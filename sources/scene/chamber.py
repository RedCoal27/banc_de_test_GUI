from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class Chamber(CustomWidget):
    def __init__(self, pos , parent):
        ratio = (0.4, 0.2)
        super().__init__(parent.translator, pos, ratio, "#00B0F0", police_size=12)
        self.create_label("chamber", alignment = Qt.AlignmentFlag.AlignCenter)