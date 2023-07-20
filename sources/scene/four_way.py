from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from internal.custom_widget import CustomWidget

from internal.logger import logger

from graph_window import GraphWindow


class FourWay(CustomWidget):
    def __init__(self, parent, pos , cmd, key ,number= ""):
        """
        Initializes a FourWay object.

        Args:
        - translator: a translator object used for internationalization
        - pos: a tuple representing the position of the widget
        - key: a string representing the key of the widget
        - number: a string representing the number of the widget (optional)
        - parent: a parent widget (optional)
        """
        ratio = (0.101, 0.23)
        super().__init__(parent.translator, pos, ratio, "#FBE5D6", None)

        self.serial_reader = parent.serial_reader
        self.FourWay_number = number
        self.state = False
        self.key = key
        self.cmd = cmd

        self.create_labels()
        self.create_buttons()
        self.update_DO()
        

    def create_labels(self):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(self.key, number = self.FourWay_number,alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.create_label("do_up", state = "false")
        self.create_label("do_down", state = "true")
        self.create_label("di_up", state = "false")
        self.create_label("di_down", state = "false")
        self.create_label("position", state = "unknown")


    def create_buttons(self):
        """
        Creates buttons for the FourWay widget.
        """
        self.create_button("change_state", self.update_DO, state = "up")
        self.create_button("cycle", self.open_windows)

    def update_DI(self, up, down):
        """
        Updates the DI labels of the FourWay widget.

        Args:
        - up: a boolean representing the state of the up DI
        - down: a boolean representing the state of the down DI
        """
        self.update_label('di_up', state = "false" if up else "true")
        self.update_label('di_down', state = "false" if down else "true")
        self.update_label('position', state = "unknown" if up*2 == down else "up" if not up else "down")

    def update_DO(self):
        """
        Updates the DO labels of the FourWay widget.
        """
        if self.serial_reader.ser is not None:
            self.state = not self.state

            self.serial_reader.write_data(self.cmd, not self.state)
            self.update_label('do_up', state = "false" if self.state else "true")
            self.update_label('do_down', state = "true" if self.state else "false")
            self.update_button('change_state', state = "up" if self.state else "down")

            logger.debug(f"Gate {self.key} is set to {'up' if self.state else 'down'}")


    def open_windows(self):
        self.window = GraphWindow(self.translator, self.key, self.cmd, self.FourWay_number)
        self.window.show()