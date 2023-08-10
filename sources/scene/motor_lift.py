from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class MotorisedLift(CustomWidget):
    """
    La classe MotorisedLift gère un élévateur motorisé. Elle hérite de la classe CustomWidget.

    Methods:
        __init__(self, pos, key, parent):
            Constructeur de la classe MotorisedLift.
        
        create_labels(self, key):
            Crée des étiquettes pour le widget MotorisedLift.

        create_buttons(self):
            Crée des boutons pour le widget MotorisedLift.
    """
    def __init__(self, pos , key , parent):
        """
        Constructeur de la classe MotorisedLift.

        Args:
            pos: La position du widget.
            key: La clé utilisée pour identifier l'élévateur motorisé.
            parent: La référence à l'objet parent du widget.
        """
        ratio = (0.101, 0.18)
        super().__init__(parent.translator, pos, ratio, "#F8CBAD")
        self.create_labels(key)
        self.create_buttons()
        
    def create_labels(self,key):
        """
        Crée des étiquettes pour le widget MotorisedLift.

        Args:
            key: La clé utilisée pour identifier l'élévateur motorisé.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("p_home", state="false")
        self.create_label("p_prcs", state="false")
        self.create_label("steps", state="false")
        self.create_label("cmd", state="")

    def create_buttons(self):
        """
        Crée des boutons pour le widget MotorisedLift.
        """
        self.create_button("cycle")
