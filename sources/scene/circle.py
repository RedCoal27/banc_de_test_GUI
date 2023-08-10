from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem

class Circle(QGraphicsEllipseItem):
    """
    Cette classe représente un QGraphicsEllipseItem personnalisé qui conserve sa taille en fonction d'un ratio.

    Args:
        x (float): La coordonnée x du centre du cercle.
        y (float): La coordonnée y du centre du cercle.
        radius (float): Le rayon du cercle.
        color (str): La couleur du cercle au format hexadécimal (par exemple, "#FFFFFF").
        left_click_function (function, optionnel): La fonction à appeler lorsque le cercle est cliqué avec le bouton gauche. Par défaut, None.
        right_click_function (function, optionnel): La fonction à appeler lorsque le cercle est cliqué avec le bouton droit. Par défaut, None.
        parent (QGraphicsItem, optionnel): L'élément parent. Par défaut, None.
    """

    def __init__(self, x, y, radius, color, left_click_function=None, right_click_function=None, parent=None):
        """
        Un QGraphicsEllipseItem personnalisé qui conserve sa taille en fonction d'un ratio.

        Args:
            x (float): La coordonnée x du centre du cercle.
            y (float): La coordonnée y du centre du cercle.
            radius (float): Le rayon du cercle.
            color (str): La couleur du cercle au format hexadécimal (par exemple, "#FFFFFF").
            left_click_function (function, optionnel): La fonction à appeler lorsque le cercle est cliqué avec le bouton gauche. Par défaut, None.
            right_click_function (function, optionnel): La fonction à appeler lorsque le cercle est cliqué avec le bouton droit. Par défaut, None.
            parent (QGraphicsItem, optionnel): L'élément parent. Par défaut, None.
        """
        self.center = (x, y)
        self.radius = radius
        super(Circle, self).__init__(parent)
        self.setRect(x - radius, y - radius, radius * 2, radius * 2 * 1.1)
        self.color = color
        self.setPen(QPen(QColor(self.color), 2))
        self.setBrush(QBrush(Qt.GlobalColor.white))
        self.setAcceptHoverEvents(True)
        self.left_click_function = left_click_function
        self.right_click_function = right_click_function

    def set_pos_size(self, width, height):
        """
        Définit la position et la taille du cercle.

        Args:
            width (int): La largeur du widget parent.
            height (int): La hauteur du widget parent.
        """
        self.setRect(self.center[0] * width - self.radius * width, self.center[1] * height - self.radius * height * 1.2, self.radius * 2 * width, self.radius * 2 * height * 1.2)
        self.setPen(QPen(QColor(self.color), 2))
        self.setBrush(QBrush(Qt.GlobalColor.white))

    def hoverEnterEvent(self, event):
        """
        Modifie le curseur en une main pointant lorsque la souris entre dans le cercle.
        """
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        """
        Change le curseur en flèche lorsque la souris quitte le cercle.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        """
        Appelle la fonction associée au cercle lorsque celui-ci est cliqué.
        """
        if event.button() == Qt.MouseButton.LeftButton and self.left_click_function is not None:
            self.left_click_function()

    def setRightClickFunction(self, function):
        """
        Définit la fonction à appeler lorsque le cercle est cliqué avec le bouton droit.

        Args:
            function (function): La fonction à appeler.
        """
        self.right_click_function = function

    def contextMenuEvent(self, event):
        """
        Crée un menu contextuel personnalisé (menu clic droit) pour le cercle.
        """
        if self.right_click_function is not None:
            self.right_click_function(event)
