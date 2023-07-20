from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsLineItem


class Line(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, color, parent=None):
        """
        A custom QGraphicsLineItem that retains its size based on a ratio.

        Args:
            x1 (float): The x coordinate of the starting point.
            y1 (float): The y coordinate of the starting point.
            x2 (float): The x coordinate of the ending point.
            y2 (float): The y coordinate of the ending point.
            color (str): The color of the line in hexadecimal format (e.g. "#FFFFFF").
            ratio (tuple): A tuple containing the x and y ratios of the line's length relative to the parent widget's width and height.
            parent (QGraphicsItem, optional): The parent item. Defaults to None.
        """
        self.position = (x1, y1)
        self.position2 = (x2, y2)
        super(Line, self).__init__(parent)
        self.color = color
        self.setPen(QPen(QColor(self.color), 3))

    def set_line(self,scene, x1, y1, x2, y2):
        self.position = (x1, y1)
        self.position2 = (x2, y2)
        self.setLine(self.position[0]*scene.width(), self.position[1]*scene.height(), self.position2[0]*scene.width(), self.position2[1]*scene.height() )

    def set_pos_size(self, width, height, scale_factor=None):
        """
        Sets the position and size of the line.

        Args:
            width (int): The width of the parent widget.
            height (int): The height of the parent widget.
        """
        self.setLine(self.position[0] * width, self.position[1] * height, self.position2[0] * width, self.position2[1] * height )
        self.setPen(QPen(QColor(self.color), 3))
