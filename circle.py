from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsEllipseItem


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, color, function=None, parent=None):
        """
        A custom QGraphicsEllipseItem that retains its size based on a ratio.

        Args:
            x (float): The x coordinate of the center of the circle.
            y (float): The y coordinate of the center of the circle.
            radius (float): The radius of the circle.
            color (str): The color of the circle in hexadecimal format (e.g. "#FFFFFF").
            function (function, optional): The function to be called when the circle is clicked. Defaults to None.
            parent (QGraphicsItem, optional): The parent item. Defaults to None.
        """
        self.center = (x, y)
        self.radius = radius
        super(Circle, self).__init__(parent)
        self.setRect(x- radius, y - radius, radius * 2, radius * 2)
        self.color = color
        self.setPen(QPen(QColor(self.color), 2))
        self.setBrush(QBrush(Qt.white))
        self.setAcceptHoverEvents(True)
        self.function = function


    def set_pos_size(self, width, height, scale_factor):
        """
        Sets the position and size of the circle.

        Args:
            width (int): The width of the parent widget.
            height (int): The height of the parent widget.
            scale_factor (float): The scale factor to be applied to the circle's pen width.
        """
        self.setRect(self.center[0] * width - self.radius * width, self.center[1] * height - self.radius * height*1.2, self.radius * 2 * width, self.radius * 2 * height*1.2)
        self.setPen(QPen(QColor(self.color), 2 * scale_factor))
        self.setBrush(QBrush(Qt.white))

    def hoverEnterEvent(self, event):
        """
        Changes the cursor to a pointing hand when the mouse enters the circle.
        """
        self.setCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        """
        Changes the cursor back to an arrow when the mouse leaves the circle.
        """
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        """
        Calls the function associated with the circle when it is clicked.
        """
        if self.function is not None:
            self.function()