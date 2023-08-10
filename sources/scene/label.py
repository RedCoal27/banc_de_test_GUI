from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class Label(CustomWidget):
    """
    La classe Label hérite de CustomWidget et représente un widget d'étiquette personnalisé. Elle crée une étiquette avec un texte spécifié et l'ajoute à la scène parent.

    Methods:
        __init__(self, pos, ratio , key , parent):
            Initialise un objet Label avec la position, le rapport, la clé et le parent donnés. Crée une étiquette avec le texte spécifié et l'ajoute à la scène parente.

    Attributes:
        scene: Référence à la scène parente dans laquelle l'étiquette est ajoutée.

    Components:
        labels: Un dictionnaire d'étiquettes associées au widget Label.
            key: QLabel affichant le texte spécifié.
    """
    def __init__(self, pos, ratio , key , parent):
        """
        Initialise un objet Label avec la position, le rapport, la clé et le parent spécifiés. Crée une étiquette avec le texte spécifié et l'ajoute à la scène parente.

        Args:
            pos: Position du widget dans le parent.
            ratio: Rapport de largeur et de hauteur du widget.
            key: Texte à afficher dans l'étiquette.
            parent: Référence au widget parent contenant ce widget Label.
        """
        super().__init__(parent.translator, pos, ratio, "#FFFFFF")
        self.create_label(key, color="#8FAADC", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.scene = parent.scene
        self.scene.addItem(self)
