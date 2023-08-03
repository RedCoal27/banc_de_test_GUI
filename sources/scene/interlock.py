from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

class Interlock(CustomWidget):
    def __init__(self, pos , key , parent):
        ratio = (0.15, 0.10)
        super().__init__(parent.translator, pos, ratio, "#FFD966")
        self.states = []
        self.create_labels(key)
        
    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_indicator("roughing_pump_state")
        self.create_label_with_indicator("pump_pressure_high")
        self.create_label_with_indicator("chamber_open")
        self.create_label_with_indicator("chamber_pressure_high")

    def update_interlock(self, states):
        """
        Updates the labels of the FourWay widget.

        Args:
        - states: liste of booleans representing the state of the indicators
        """
        for indicator, _ in self.indicators:
            self.update_indicator(indicator, states.pop(0))
