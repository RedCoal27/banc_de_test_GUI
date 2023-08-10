from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem

class Line(QGraphicsLineItem):
    """
    La classe Line hérite de QGraphicsLineItem et représente un widget personnalisé de ligne. Elle crée une ligne avec des coordonnées spécifiées et la conserve à l'échelle en fonction d'un ratio.

    Methods:
        __init__(self, x1, y1, x2, y2, color, width=3, parent=None):
            Initialise un objet Line avec les coordonnées de début, les coordonnées de fin, la couleur, la largeur et le parent spécifiés. Crée une ligne avec les propriétés spécifiées.

        set_line(self, scene, x1, y1, x2, y2):
            Définit les coordonnées de la ligne en fonction de la scène donnée et des nouvelles coordonnées.

        set_pos_size(self, width, height):
            Définit la position et la taille de la ligne en fonction de la largeur et de la hauteur du widget parent.

    Attributes:
        position: Coordonnées du point de départ de la ligne.
        position2: Coordonnées du point d'arrêt de la ligne.
        color: Couleur de la ligne.
        width: Largeur de la ligne.
    """
    def __init__(self, x1, y1, x2, y2, color, width=3, parent=None):
        """
        Initialise un objet Line avec les coordonnées de début, les coordonnées de fin, la couleur, la largeur et le parent spécifiés. Crée une ligne avec les propriétés spécifiées.

        Args:
            x1: Coordonnée x du point de départ.
            y1: Coordonnée y du point de départ.
            x2: Coordonnée x du point d'arrêt.
            y2: Coordonnée y du point d'arrêt.
            color: Couleur de la ligne au format hexadécimal (par exemple, "#FFFFFF").
            width: Largeur de la ligne. Par défaut, 3.
            parent: Élément parent. Par défaut, None.
        """
        self.position = (x1, y1)
        self.position2 = (x2, y2)
        super(Line, self).__init__(parent)
        self.color = color
        self.width = width
        self.setPen(QPen(QColor(self.color), self.width))

    def set_line(self, scene, x1, y1, x2, y2):
        """
        Définit les coordonnées de la ligne en fonction de la scène donnée et des nouvelles coordonnées.

        Args:
            scene: Scène dans laquelle la ligne est affichée.
            x1: Coordonnée x du point de départ.
            y1: Coordonnée y du point de départ.
            x2: Coordonnée x du point d'arrêt.
            y2: Coordonnée y du point d'arrêt.
        """
        self.position = (x1, y1)
        self.position2 = (x2, y2)
        self.setLine(self.position[0] * scene.width(), self.position[1] * scene.height(), self.position2[0] * scene.width(), self.position2[1] * scene.height())

    def set_pos_size(self, width, height):
        """
        Définit la position et la taille de la ligne en fonction de la largeur et de la hauteur du widget parent.

        Args:
            width: Largeur du widget parent.
            height: Hauteur du widget parent.
        """
        self.setLine(self.position[0] * width, self.position[1] * height, self.position2[0] * width, self.position2[1] * height)
