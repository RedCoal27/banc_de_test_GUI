from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class Interlock(CustomWidget):
    """
    Cette classe représente un widget Interlock. Elle hérite de CustomWidget et permet de contrôler un ensemble d'indicateurs de l'interlock.

    Args:
        pos: Tuple représentant la position du widget.
        key: Clé utilisée pour identifier le widget.
        parent: Objet parent du widget.

    Attributes:
        parent: Objet parent du widget.
        states: Liste des états des indicateurs de l'interlock.

    Methods:
        __init__(self, pos, key, parent):
            Initialise un objet Interlock.

        create_labels(self, key):
            Crée les étiquettes pour le widget.

        update_interlock(self, states):
            Met à jour les étiquettes et les indicateurs du widget.

        get_value(self):
            Récupère la valeur du widget. Utilisée dans la recette.
        
    Components:
        labels: Dictionnaire d'étiquettes pour afficher des informations liées à la chambre
            roughing_pump_state: État de la pompe de roughing.
            pump_pressure_high: Pression de la pompe de roughing trop élevée.
            chamber_open: Chambre ouverte.
            chamber_pressure_high: Pression de la chambre trop élevée.
            
        indicators: Dictionnaire d'indicateurs pour afficher l'état des composants de la chambre.
            roughing_pump_state: État de la pompe de roughing.
            pump_pressure_high: Pression de la pompe de roughing trop élevée.
            chamber_open: Chambre ouverte.
            chamber_pressure_high: Pression de la chambre trop élevée.
    """

    def __init__(self, pos, key, parent):
        """
        Initialise un objet Interlock.

        Args:
            pos: Tuple représentant la position du widget.
            key: Clé utilisée pour identifier le widget.
            parent: Objet parent du widget.
        """
        ratio = (0.15, 0.10)
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#FFD966")
        self.states = []
        self.create_labels(key)

    def create_labels(self, key):
        """
        Crée les étiquettes pour le widget.

        Args:
            key: Clé utilisée pour identifier le widget.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_indicator("roughing_pump_state", state="On")
        self.create_label_with_indicator("pump_pressure_high", sens="<", value=self.parent.config["pump_pressure"]["setpoint_low"])
        self.create_label_with_indicator("chamber_open", state="close")
        self.create_label_with_indicator("chamber_pressure_high", sens="<", value=self.parent.config["chamber_pressure"]["setpoint_low"])

    def update_interlock(self, states):
        """
        Met à jour les étiquettes et les indicateurs du widget.

        Args:
            states: Liste de booléens représentant l'état des indicateurs de l'interlock.
        """
        self.states = states
        self.update_indicator(self, "roughing_pump_state", states[0])
        self.update_indicator(self, "pump_pressure_high", states[1])
        self.update_indicator(self, "chamber_open", states[2])
        self.update_indicator(self, "chamber_pressure_high", states[3])

        self.update_label("roughing_pump_state", state="off" if states[0] else "on")
        self.update_label("pump_pressure_high", sens=">" if states[0] else "<", value=self.parent.config["pump_pressure"]["setpoint_low"])
        self.update_label("chamber_open", state="open" if states[0] else "close")
        self.update_label("chamber_pressure_high", sens=">" if states[0] else "<", value=self.parent.config["chamber_pressure"]["setpoint_low"])

    def get_value(self):
        """
        Récupère la valeur du widget. Utilisée dans la recette.
        """
        value = 0
        for i, state in enumerate(self.states):
            if state:
                value += 2 ** i
        return value
