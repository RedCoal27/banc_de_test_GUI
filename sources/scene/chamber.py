from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class Chamber(CustomWidget):
    """
    Cette classe représente un widget personnalisé appelé 'Chamber', qui hérite de 'CustomWidget'. Elle crée un widget spécialisé avec une étiquette pour afficher des informations liées à la chambre.

    Args:
        pos: Tuple d'entiers représentant les positions x et y du widget.
        parent: Widget parent auquel appartient ce widget Chamber.

    Attributes:
        ratio: Tuple de flottants représentant le rapport largeur/hauteur du widget.
        font_size: Entier représentant la taille de police du widget.
        color: Chaîne représentant la couleur du widget.

    Methods:
        __init__(self, pos, parent):
            Initialise un widget Chamber avec la position et le parent donnés. Définit le ratio, la couleur et la taille de police.

        set_font_size(self, size):
            Définit la taille de police du widget.

    Components:
        labels: Dictionnaire d'étiquettes pour afficher des informations liées à la chambre.
            chamber: Étiquette pour afficher les informations liées à la chambre.
    """

    def __init__(self, pos, parent):
        """
        Initialise un widget Chamber avec la position et le parent spécifiés. Définit le ratio, la couleur et la taille de police du widget.

        Args:
            pos: Tuple d'entiers représentant les positions x et y du widget.
            parent: Widget parent auquel appartient ce widget Chamber.
        """
        ratio = (0.4, 0.2)
        super().__init__(parent.translator, pos, ratio, "#00B0F0", font_size=12)
        self.create_label("chamber", alignment=Qt.AlignmentFlag.AlignCenter)

    def set_font_size(self, size):
        """
        Définit la taille de police du widget.

        Args:
            size: Entier représentant la nouvelle taille de police.
        """
        self.font_size = size + 2
