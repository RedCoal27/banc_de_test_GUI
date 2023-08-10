from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class IonGauge(CustomWidget):
    """
    Cette classe représente un widget IonGauge. Elle hérite de CustomWidget et permet de contrôler un indicateur de jauge ionique.

    Args:
        pos: Tuple représentant la position du widget.
        key: Clé utilisée pour identifier le widget.
        parent: Objet parent du widget.

    Methods:
        __init__(self, pos, key, parent):
            Initialise un objet IonGauge.

        create_labels(self, key):
            Crée les étiquettes pour le widget.
    
    Components:
        labels :
            command: Étiquette affichant la commande envoyée à l'indicateur de jauge ionique.
            reading: Étiquette affichant la lecture de l'indicateur de jauge ionique.
            pressure: Étiquette affichant la pression de l'indicateur de jauge ionique. 
    """

    def __init__(self, pos , key , parent):
        """
        Initialise un objet IonGauge.

        Args:
            pos: Tuple représentant la position du widget.
            key: Clé utilisée pour identifier le widget.
            parent: Objet parent du widget.
        """
        ratio = (0.12, 0.10)
        super().__init__(parent.translator, pos, ratio, "#E2F0D9")
        self.create_labels(key)
        

    def create_labels(self, key):
        """
        Crée les étiquettes pour le widget.

        Args:
            key: Clé utilisée pour identifier le widget.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.create_label("command", value="off")
        self.create_label("reading", value="off")
        self.create_label("pressure", value="RS485")
