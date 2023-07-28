from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu, QAction


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, color, left_click_function=None, right_click_function=None, parent=None):
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
        self.setBrush(QBrush(Qt.GlobalColor.white))
        self.setAcceptHoverEvents(True)
        self.left_click_function = left_click_function
        self.right_click_function = right_click_function


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
        self.setBrush(QBrush(Qt.GlobalColor.white))

    def hoverEnterEvent(self, event):
        """
        Changes the cursor to a pointing hand when the mouse enters the circle.
        """
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        """
        Changes the cursor back to an arrow when the mouse leaves the circle.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        """
        Calls the function associated with the circle when it is clicked.
        """
        if event.button() == Qt.MouseButton.LeftButton and self.left_click_function is not None:
                self.left_click_function()

    def setRightClickFunction(self, function):
        """
        Sets the function to be called when the circle is right clicked.

        Args:
            function (function): The function to be called.
        """
        self.right_click_function = function

    def contextMenuEvent(self, event):
        """
        Creates a custom context menu (right click menu) for the circle.
        """
        if self.right_click_function is not None:
            self.right_click_function(event)