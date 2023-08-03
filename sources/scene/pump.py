from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget
from internal.logger import Logger

class Pump(CustomWidget):
    def __init__(self, pos, cmd, key , parent):
        ratio = (0.1, 0.14)
        self.serial_reader = parent.serial_reader
        self.state = True
        self.cmd = cmd
        self.key = key
        super().__init__(parent.translator, pos, ratio, "#FF0000")
        self.create_labels(key)
        self.create_button("set_state", self.click_DO, state = "off")
        self.update_DO()
        

    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("cmd", state = "false")
        self.create_label("status", state = "false")
        self.create_label("accelerate", state = "false")

    def update_DI(self, status):
        """
        Updates the DI labels of the FourWay widget.

        Args:
        - status: a boolean representing the state of the status DI
        """
        self.update_label('status', state = "slow" if status else "at_speed")


    def update_DO(self, new_state = None):
        """
        Updates the DO buttons of the FourWay widget.
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state

            self.serial_reader.write_data(self.cmd, not self.state)
            self.update_label('cmd', state = "on" if self.state else "off")
            self.update_button("set_state", state = "on" if self.state else "off")

            Logger.debug(f"{self.key} is turn {'on' if self.state else 'off'}")

    def click_DO(self):
        self.update_DO()
