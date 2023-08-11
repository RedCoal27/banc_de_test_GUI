from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class ThrottleValve(CustomWidget):
    """
    La classe ThrottleValve gère une Throttle Valve. Elle hérite de la classe CustomWidget.

    Methods:
        __init__(self, pos, key, parent):
            Constructeur de la classe ThrottleValve.

        create_labels(self, key):
            Crée des étiquettes pour le widget ThrottleValve.

        create_buttons(self):
            Crée des boutons pour le widget ThrottleValve.
    
    Components:
        labels: Un dictionnaire contenant les étiquettes du widget.
            open: Étiquette indiquant l'état de la vanne.
            close: Étiquette indiquant l'état de la vanne.
            steps: Étiquette indiquant le nombre de pas de la vanne.
            hysteresis: Étiquette indiquant l'hystérésis de la vanne.
            cmd: Étiquette indiquant la commande de la vanne.
        buttons: Un dictionnaire contenant les boutons du widget.
            cycle: Bouton permettant de faire un cycle de la vanne.
    """
    def __init__(self, pos, key, parent):
        """
        Constructeur de la classe ThrottleValve.

        Args:
            pos: Position du widget.
            key: Clé utilisée pour identifier la vanne.
            parent: Référence à l'objet parent du widget.
        """
        ratio = (0.11, 0.25)
        super().__init__(parent.translator, pos, ratio, "#F8CBAD")
        self.create_labels(key)
        self.create_buttons()
        

    def create_labels(self, key):
        """
        Crée des étiquettes pour le widget ThrottleValve.

        Args:
            key: Clé utilisée pour identifier la vanne.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("open", state="false")
        self.create_label("close", state="false")
        self.create_label("steps", state="false")
        self.create_label("hysteresis", state="")
        self.create_label("cmd", state="false")

    def create_buttons(self):
        """
        Crée des boutons pour le widget ThrottleValve.
        """
        self.create_button("cycle")


    def relative_move(self):
        z

    def Home(self):
        data = relative_move(100)
        data = relative_move(-1000)