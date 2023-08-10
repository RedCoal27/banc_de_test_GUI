from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

class RoughingPump(CustomWidget):
    """
    La classe RoughingPump gère une pompe primaire. Elle hérite de la classe CustomWidget.

    Attributes:
        serial_reader: Référence à l'objet de lecture série.
        state: État de la pompe (activée ou désactivée).
        cmd: Commande utilisée pour activer ou désactiver la pompe.
        key: Clé utilisée pour identifier la pompe.
    
    Methods:
        __init__(self, pos, cmd, key, parent):
            Constructeur de la classe RoughingPump.

        create_labels(self, key):
            Crée des étiquettes pour le widget RoughingPump.

        update_DI(self, status):
            Met à jour les étiquettes DI du widget RoughingPump.

        update_DO(self, new_state=None):
            Met à jour les boutons DO du widget RoughingPump.

        click_DO(self):
            Gère le clic sur le bouton pour activer ou désactiver la pompe.

        set_value(self, value):
            Définit la valeur de la pompe primaire. Utilisé pour les recettes.

        get_value(self):
            Renvois la valeur de la pompe primaire. Utilisé pour les recettes.

        Components:
            labels: Un dictionnaire contenant les étiquettes du widget.
                cmd: Étiquette pour l'état de la commande.
                status: Étiquette pour l'état de la pompe.
                Error: Étiquette pour l'état d'erreur.
            buttons: Un dictionnaire contenant les boutons du widget.
                set_state: Bouton pour activer ou désactiver la pompe.
    """
    def __init__(self, pos, cmd, key, parent):
        """
        Constructeur de la classe RoughingPump.

        Args:
            pos: Position du widget.
            cmd: Commande utilisée pour activer ou désactiver la pompe.
            key: Clé utilisée pour identifier la pompe.
            parent: Référence à l'objet parent du widget.
        """
        ratio = (0.1, 0.14)
        self.serial_reader = parent.serial_reader
        self.state = True
        self.cmd = cmd
        self.key = key
        super().__init__(parent.translator, pos, ratio, "#4472C4")
        self.create_labels(key)
        self.create_button("set_state", self.click_DO, state="off")
        self.update_DO()

    def create_labels(self, key):
        """
        Crée des étiquettes pour le widget RoughingPump.

        Args:
            key: Clé utilisée pour identifier la pompe.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("cmd", state="false")
        self.create_label("status", state="false")
        self.create_label("Error", state="false")

    def update_DI(self, status):
        """
        Met à jour les étiquettes DI du widget RoughingPump.

        Args:
            status: Un booléen représentant l'état du DI de statut.
        """
        self.update_label('status', state="false" if status else "true")

    def update_DO(self, new_state=None):
        """
        Met à jour les boutons DO du widget RoughingPump.

        Args:
            new_state: Nouvel état de la pompe (optionnel).
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state

            self.serial_reader.write_data(self.cmd, not self.state)
            self.update_label('cmd', state="on" if self.state else "off")
            self.update_button("set_state", state="on" if self.state else "off")

            Logger.debug(f"{self.key} is turned {'on' if self.state else 'off'}")

    def click_DO(self):
        """
        Gère le clic sur le bouton pour activer ou désactiver la pompe.
        """
        self.update_DO()

    def set_value(self, value):
        """
        Définit la valeur de la pompe primaire. Utilisé pour les recettes.

        Args:
            value: La valeur de la pompe (activée ou désactivée).
        """
        self.update_DO(value)

    def get_value(self):
        """
        Renvois la valeur de la pompe primaire. Utilisé pour les recettes.
        """
        return self.state
