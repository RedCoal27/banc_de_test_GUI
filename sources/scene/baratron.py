from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

class Baratron(CustomWidget):
    """
    La classe Baratron représente un composant d'interface utilisateur lié à un Baratron. Elle hérite de la classe CustomWidget.

    Attributes:
        offset: Valeur de l'offset pour le Baratron.
        key: Clé associée au widget Baratron.
        value: Valeur actuelle du Baratron.

    Methods:
        __init__(self, pos, key, parent):
            Initialise le widget Baratron avec la position, la clé et le parent donnés. Configure les attributs et crée des étiquettes.

        create_labels(self, key):
            Crée des étiquettes pour le widget Baratron.

        update_AI(self, value):
            Met à jour la valeur de l'étiquette du Baratron avec une logique spécifique.

        update_offset(self, spin_box):
            Met à jour l'offset pour le Baratron.

        get_value(self):
            Renvoie la valeur actuelle du Baratron.
    
    Components:
        labels: Un dictionnaire d'étiquettes associées au widget Baratron.
            pressure: L'étiquette pour la valeur de pression du Baratron.
            offset: L'étiquette pour l'offset du Baratron.
            size: L'étiquette pour la valeur de taille du Baratron.
        spin_boxes: Un dictionnaire de boîtes à spin associées au widget Baratron.
            offset: La boîte à spin pour l'offset du Baratron.
    """
    def __init__(self, pos, key, parent):
        """
        Initialise le widget Baratron avec la position, la clé et le parent spécifiés. Configure les attributs et crée des étiquettes.

        Args:
            pos: Position du widget.
            key: Clé associée au widget.
            parent: Parent du widget.
        """
        ratio = (0.12, 0.1)
        self.offset = 0
        self.key = key
        self.value = 0
        super().__init__(parent.translator, pos, ratio, "#C5E0B4")
        self.create_labels(key)

    def create_labels(self, key):
        """
        Crée des étiquettes pour le widget Baratron.

        Args:
            key: Une chaîne représentant la clé du widget.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("pressure", value="0", unit=" Torr")
        self.create_label_with_spin_box("offset", unit=" Torr", initial_value=0, min_value=-100, max_value=100, function=self.update_offset)
        self.create_label("size", value="0.1", unit=" Torr")

    def update_AI(self, value):
        """
        Met à jour la valeur de l'étiquette du Baratron avec une logique spécifique.

        Args:
            value: La valeur à mettre à jour dans l'étiquette.
        """
        unit = " Torr"
        value = float(value)
        if value > 10.5:
            value = "surcharge"
            unit = ""
        else:
            value = value * 0.1 / 10 - self.offset
            value = f"{value:.2e}"  # Notation scientifique avec 1 décimale
            base, exp = value.split("e")
            if len(exp) == 3:
                exp = exp[0] + exp[2]
            value = base + "E" + exp
        self.value = value
        self.update_label("pressure", value=value, unit=unit)

    def update_offset(self, spin_box):
        """
        Met à jour l'offset pour le Baratron.

        Args:
            spin_box: Le widget de boîte à spin qui fournit l'offset.
        """
        Logger.debug(f"{self.key} offset modifié en {spin_box.value()}")
        self.offset = spin_box.value()

    def get_value(self):
        """
        Renvoie la valeur actuelle du Baratron.

        Returns:
            float: La valeur actuelle, avec une gestion spécifique pour "surcharge".
        """
        if self.value == "surcharge":
            return 1000
        else:
            return float(self.value)
