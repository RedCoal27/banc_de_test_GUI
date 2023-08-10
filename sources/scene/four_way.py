from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

from internal.logger import Logger

from window.graph_window import GraphWindow

class FourWay(CustomWidget):
    """
    Cette classe représente un widget FourWay. Elle hérite de CustomWidget et permet de contrôler un dispositif à quatre voies.

    Args:
        pos: Tuple représentant la position du widget.
        cmd: Objet de commande utilisé pour la communication avec le matériel.
        key: Chaîne représentant la clé du widget.
        number: Chaîne représentant le numéro du widget (facultatif).
        parent: Widget parent (facultatif).

    Attributes:
        serial_reader: Objet de lecteur série pour la communication.
        FourWay_number: Numéro du widget FourWay.
        state: État actuel du dispositif.
        key: Clé du widget FourWay.
        cmd: Objet de commande utilisé pour la communication avec le matériel.
        sensor_up: État du capteur supérieur.
        sensor_down: État du capteur inférieur.
        parent: Widget parent.

    Methods:
        __init__(self, pos, cmd, key, parent, number=""):
            Initialise un objet FourWay.

        create_labels(self):
            Crée des étiquettes pour le widget FourWay.

        create_buttons(self):
            Crée des boutons pour le widget FourWay.

        update_DI(self, up, down):
            Met à jour les étiquettes DI du widget FourWay.

        update_DO(self, new_state=None):
            Met à jour les étiquettes DO du widget FourWay.

        click_DO(self):
            Fonction de rappel pour le bouton set_state. Met à jour les étiquettes DO du widget FourWay.

        open_windows(self):
            Fonction de rappel pour le bouton cycle. Ouvre un objet GraphWindow.

        set_value(self, value):
            Définit la valeur du FourWay. Utilisé pour les recettes.

        get_value(self):
            Récupère la valeur de la vanne. Utilisé pour les recettes.

    Components:
        labels: Dictionnaire contenant les étiquettes du widget.
            do_up : Étiquette représentant l'état du DO supérieur.
            do_down : Étiquette représentant l'état du DO inférieur.
            di_up : Étiquette représentant l'état du DI supérieur.
            di_down : Étiquette représentant l'état du DI inférieur.
            position : Étiquette représentant la position de la vanne.
        buttons: Dictionnaire contenant les boutons du widget.
            set_state : Bouton permettant de changer l'état du DO.
            cycle : Bouton permettant d'ouvrir un objet GraphWindow.
    """

    def __init__(self, pos, cmd, key, parent, number=""):
        """
        Initialise un objet FourWay.

        Args:
            pos: Tuple représentant la position du widget.
            cmd: Objet de commande utilisé pour la communication avec le matériel.
            key: Chaîne représentant la clé du widget.
            number: Chaîne représentant le numéro du widget (facultatif).
            parent: Widget parent (facultatif).
        """
        ratio = (0.101, 0.23)
        super().__init__(parent.translator, pos, ratio, "#FBE5D6")

        self.serial_reader = parent.serial_reader
        self.FourWay_number = number
        self.state = False
        self.key = key
        self.cmd = cmd
        self.sensor_up = True
        self.sensor_down = True
        self.parent = parent

        self.create_labels()
        self.create_buttons()
        self.update_DO()

    def create_labels(self):
        """
        Crée des étiquettes pour le widget FourWay.
        """
        self.create_label(self.key, number=self.FourWay_number, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("do_up", state="false")
        self.create_label("do_down", state="true")
        self.create_label("di_up", state="false")
        self.create_label("di_down", state="false")
        self.create_label("position", state="unknown")

    def create_buttons(self):
        """
        Crée des boutons pour le widget FourWay.
        """
        self.create_button("set_state", self.click_DO, state="up")
        self.create_button("cycle", self.open_windows)

    def update_DI(self, up, down):
        """
        Met à jour les étiquettes DI du widget FourWay.

        Args:
            up: Booléen représentant l'état du DI supérieur.
            down: Booléen représentant l'état du DI inférieur.
        """
        self.sensor_up = up
        self.sensor_down = down
        self.update_label('di_up', state="false" if up else "true")
        self.update_label('di_down', state="false" if down else "true")
        self.update_label('position', state="unknown" if up * 2 == down else "up" if not up else "down")

    def update_DO(self, new_state=None):
        """
        Met à jour les étiquettes DO du widget FourWay.
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state

            self.serial_reader.write_data(self.cmd.DO, not self.state)
            self.update_label('do_up', state="false" if self.state else "true")
            self.update_label('do_down', state="true" if self.state else "false")
            self.update_button("set_state", state="down" if self.state else "up")

            Logger.debug(f"{self.key}{self.FourWay_number} est réglé sur {'up' if self.state else 'down'}")

    def click_DO(self):
        """
        Fonction de rappel pour le bouton set_state. Met à jour les étiquettes DO du widget FourWay.
        """
        self.update_DO()

    def open_windows(self):
        """
        Fonction de rappel pour le bouton cycle. Ouvre un objet GraphWindow.
        """
        self.window = GraphWindow(self)
        self.window.show()

    def set_value(self, value):
        """
        Définit la valeur du FourWay. Utilisé pour les recettes.

        Args:
            value: Booléen représentant la nouvelle valeur du FourWay.
        """
        self.update_DO(not value)

    def get_value(self):
        """
        Récupère la valeur de la vanne. Utilisé pour les recettes.

        Returns:
            state: Entier représentant l'état de la vanne (-1 pour inconnu, 0 pour fermée, 1 pour ouverte).
        """
        state = -1 if self.sensor_up * 2 == self.sensor_down else 1 if not self.sensor_up else 0
        return state
