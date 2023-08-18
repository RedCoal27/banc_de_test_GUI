from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget
from internal.logger import Logger

class MFC(CustomWidget):
    """
    La classe MFC gère un dispositif de débit massique (MFC). Elle hérite de la classe CustomWidget.

    Attributes:
        offset: La valeur de l'offset pour le MFC.
        key: La clé utilisée pour identifier le MFC.
        cmd: L'objet de commande utilisé pour envoyer des commandes au MFC.
        value: La valeur actuelle du débit massique.
        parent: La référence à l'objet parent du widget.

    Methods:
        __init__(self, pos, cmd, key, parent):
            Initialise l'objet MFC avec la position, la commande, la clé et le parent donnés. Configure les attributs et crée des étiquettes.

        create_labels(self, key):
            Crée des étiquettes pour le widget MFC.

        update_AI(self, value):
            Met à jour la valeur de l'étiquette "actual".

        update_AO(self, spin_box):
            Met à jour la valeur de l'étiquette "setpoint" en envoyant la commande AO.

        update_offset(self, spin_box):
            Met à jour la valeur de l'offset.

        set_value(self, value):
            Définit la valeur du MFC. Utilisé dans les recettes.

        get_value(self):
            Renvois la valeur actuelle du MFC. Utilisé dans les recettes.

    Components:
        labels: Un dictionnaire contenant les étiquettes du widget.
            setpoint: L'étiquette "setpoint" contenant la valeur de consigne du MFC.
            actual: L'étiquette "actual" contenant la valeur actuelle retourné par le MFC.
            offset: L'étiquette "offset" contenant la valeur de l'offset du MFC.
            size: L'étiquette "size" contenant la valeur de la taille du MFC.
        spin_boxes: Un dictionnaire contenant les spin boxes du widget.
            setpoint: La spin box "setpoint" contenant la valeur de consigne du MFC.
            offset: La spin box "offset" contenant la valeur de l'offset du MFC.
    """
    def __init__(self, pos, cmd, key , parent):
        """
        Initialise l'objet MFC avec la position, la commande, la clé et le parent donnés. Configure les attributs et crée des étiquettes.

        Args:
            pos: La position du widget.
            cmd: L'objet de commande utilisé pour envoyer des commandes au MFC.
            key: La clé utilisée pour identifier le MFC.
            parent: La référence à l'objet parent du widget.
        """
        ratio = (0.1, 0.12)
        self.offset = 0
        self.key = key
        self.cmd = cmd
        self.value = 0
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#B4C7E7")
        self.create_labels(key)

    def create_labels(self,key):
        """
        Crée des étiquettes pour le widget MFC.

        Args:
            key: La clé utilisée pour identifier le MFC.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_spin_box("setpoint", initial_value=0, max_value=self.parent.config.get_constant_value(key), unit="sccm", function=self.update_AO)
        self.create_label("actual", value="0", unit="sccm")
        self.create_label_with_spin_box("offset", unit="sccm", initial_value=0, min_value=-100, max_value=100, function=self.update_offset)
        self.create_label("size", value=self.parent.config.get_constant_value(key), unit="sccm")

    def update_AI(self, value):
        """
        Met à jour la valeur de l'étiquette "actual".

        Args:
            value: La nouvelle valeur du débit massique.
        """
        value = (float(value)/5*self.parent.config.get_constant_value(self.key))
        self.value = int(round(value - self.offset))
        self.update_label("actual", value=self.value, unit="sccm")

    def update_AO(self, spin_box):
        """
        Met à jour la valeur de l'étiquette "setpoint" en envoyant la commande AO.

        Args:
            spin_box: L'objet spin box contenant la nouvelle valeur.
        """
        if spin_box.value() > 0: #open gate if new value is > 0
            self.parent.custom_widgets["nupro_final"].set_value(0)
            self.parent.custom_widgets[f"nupro_{self.key}"].set_value(0)

        value = spin_box.value()/self.parent.config.get_constant_value(self.key)*5  # transformer la valeur en plage 0-5V
        self.parent.serial_reader.send_data(self.cmd, value)  
        Logger.debug(f"{self.key} setpoint changed to {spin_box.value()}")


        
    def update_offset(self, spin_box):
        """
        Met à jour la valeur de l'offset.

        Args:
            spin_box: L'objet spin box contenant la nouvelle valeur.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()

    def set_value(self, value):
        """
        Définit la valeur du MFC. Utilisé dans les recettes.

        Args:
            value: La nouvelle valeur du MFC.
        """
        # Changer la valeur de la spin box
        for spin_box, spin_box_key, _, spin_box_kwargs in self.spin_boxes:
            if spin_box_key == "setpoint":
                spin_box.setValue(value)
                self.update_AO(spin_box)
                break



    def get_value(self):
        """
        Renvois la valeur actuelle du MFC. Utilisé dans les recettes.

        Returns:
            La valeur actuelle du MFC.
        """
        return self.value
