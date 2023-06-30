from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget

class FourWay(CustomWidget):
    def __init__(self, translator, pos , key , number= "" , parent=None):
        ratio = [0.1, 0.15]
        self.FourWay_number = number
        super().__init__(translator, pos, ratio, parent=None)
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self,key):
        self.create_label(key, number = self.FourWay_number,alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("do_up")
        self.create_label("do_down")
        self.create_label("di_up")
        self.create_label("di_down")



    def create_buttons(self):
        self.create_button("aaa")

