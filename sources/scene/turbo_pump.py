from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

class TurboPump(CustomWidget):
    """
    La classe TurboPump gère une pompe turbomoléculaire. Elle hérite de la classe CustomWidget.

    Attributes:
        serial_reader: Référence à l'objet pour la lecture série.
        state: État actuel de la pompe (allumée ou éteinte).
        cmd: Commande associée à la pompe.
        key: Clé utilisée pour identifier la pompe.
        status: Statut actuel de la pompe (lente ou à vitesse normale).

    Methods:
        __init__(self, pos, cmd, key, parent):
            Constructeur de la classe TurboPump.

        create_labels(self, key):
            Crée des étiquettes pour le widget TurboPump.

        update_DI(self, status):
            Met à jour les étiquettes DI du widget TurboPump.

        update_DO(self, new_state=None):
            Met à jour les boutons DO du widget TurboPump.

        click_DO(self):
            Gère le clic sur le bouton DO du widget TurboPump.

        set_value(self, value):
            Définit la valeur de la pompe. Utilisée dans les recettes.

        get_value(self):
            Retourne la valeur du statut de la pompe. Utilisée dans les recettes.

    Components:
        labels: Un dictionnaire contenant les étiquettes du widget.
            cmd: Étiquette indiquant l'état de la commande de la pompe.
            status: Étiquette indiquant l'état de la pompe.
            accelerate: Étiquette indiquant l'état de la pompe (lente ou à vitesse normale).
        buttons: Un dictionnaire contenant les boutons du widget.
            set_state: Bouton permettant d'allumer ou d'éteindre la pompe.
    """
    def __init__(self, pos, cmd, key, parent):
        """
        Constructeur de la classe TurboPump.

        Args:
            pos: Position du widget.
            cmd: Commande associée à la pompe.
            key: Clé utilisée pour identifier la pompe.
            parent: Référence à l'objet parent du widget.
        """
        ratio = (0.1, 0.14)
        self.serial_reader = parent.serial_reader
        self.state = True
        self.cmd = cmd
        self.key = key
        self.status = 0
        super().__init__(parent.translator, pos, ratio, "#FD6801")
        self.create_labels(key)
        self.create_button("set_state", self.click_DO, state="off")
        self.update_DO()
        

    def create_labels(self, key):
        """
        Crée des étiquettes pour le widget TurboPump.

        Args:
            key: Clé utilisée pour identifier la pompe.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("cmd", state="false")
        self.create_label("status", state="false")
        self.create_label("accelerate", state="false")

    def update_DI(self, status):
        """
        Met à jour les étiquettes DI du widget TurboPump.

        Args:
            status: Booléen représentant l'état du DI status.
        """
        self.status = status
        self.update_label('status', state="slow" if status else "at_speed")

    def update_DO(self, new_state=None):
        """
        Met à jour les boutons DO du widget TurboPump.
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state

            self.serial_reader.write_data(self.cmd, not self.state)
            self.update_label('cmd', state="on" if self.state else "off")
            self.update_button("set_state", state="on" if self.state else "off")

            Logger.debug(f"{self.key} is turn {'on' if self.state else 'off'}")

    def click_DO(self):
        """
        Gère le clic sur le bouton DO du widget TurboPump.
        """
        self.update_DO()

    def set_value(self, value):
        """
        Définit la valeur de la pompe. Utilisée dans les recettes.

        Args:
            value: Nouvelle valeur de la pompe.
        """
        self.update_DO(value)

    def get_value(self):
        """
        Retourne la valeur du statut de la pompe. Utilisée dans les recettes.
        """
        return self.status
