from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins
import PyQt5.QtCore as QtCore

from internal.custom_widget import CustomWidget

class Label(CustomWidget):
    def __init__(self, pos, ratio , key , parent):
        super().__init__(parent.translator, pos, ratio, "#FFFFFF")
        self.create_label(key, color="#8FAADC", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.scene = parent.scene
        self.scene.addItem(self)





