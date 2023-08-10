from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

class Generator(CustomWidget):
    """
    Cette classe représente un widget Generator. Elle hérite de CustomWidget et permet de contrôler un générateur.

    Args:
        pos: Tuple représentant la position du widget.
        cmd: Objet de commande utilisé pour envoyer des commandes au générateur.
        key: Clé utilisée pour identifier le générateur.
        parent: Objet parent du widget.

    Attributes:
        serial_reader: Objet de lecteur série pour la communication.
        key: Clé du générateur.
        cmd: Objet de commande utilisé pour envoyer des commandes au générateur.
        state: État actuel du générateur.
        interlock_state: État actuel de l'interlock du générateur.
        source_value: Valeur source actuelle du générateur.
        voltage_reflected: Tension réfléchie actuelle du générateur.
        parent: Objet parent.

    Methods:
        __init__(self, pos, cmd, key, parent):
            Initialise un objet Generator.

        create_labels(self, key):
            Crée les étiquettes pour le widget.

        create_buttons(self):
            Crée les boutons pour le widget.

        interlock(self, new_state=None):
            Définit l'état de l'interlock du générateur.

        click_interlock(self):
            Gère l'événement de clic pour le bouton de l'interlock.

        on_off(self, new_state=None):
            Allume ou éteint le générateur.

        click_on_off(self):
            Gère l'événement de clic pour le bouton marche/arrêt.

        config(self):
            Ouvre la fenêtre de configuration pour le générateur.

        update_AI(self, value):
            Met à jour la valeur AI du générateur.

        update_AO(self, spin_box):
            Met à jour la valeur AO du générateur.

        update_offset(self, spin_box):
            Met à jour la valeur de l'offset du générateur.

        set_value(self, value):
            Définit la valeur du générateur.

        get_value(self):
            Récupère la valeur actuelle du générateur.

    Components:
        labels: Dictionnaire d'étiquettes pour afficher des informations liées à la chambre.
            setpoint: Étiquette pour afficher la valeur de consigne du générateur.
            source_power: Étiquette pour afficher la valeur source du générateur.
            voltage_reflected: Étiquette pour afficher la tension réfléchie du générateur.
        buttons: Dictionnaire de boutons pour contrôler le générateur.
            interlock_state: Bouton pour activer/désactiver l'interlock du générateur.
            set_state: Bouton pour allumer/éteindre le générateur.
            config: Bouton pour ouvrir la fenêtre de configuration du générateur.
    """

    def __init__(self, pos, cmd, key, parent):
        """
        Initialise un objet Generator.

        Args:
            pos: Tuple représentant la position du widget.
            cmd: Objet de commande utilisé pour envoyer des commandes au générateur.
            key: Clé utilisée pour identifier le générateur.
            parent: Objet parent du widget.
        """
        ratio = (0.1225, 0.15)
        self.serial_reader = parent.serial_reader
        self.key = key
        self.cmd = cmd
        self.state = False
        self.interlock_state = False
        self.source_value = 0
        self.voltage_reflected = 0
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#B4C7E7")
        self.create_labels(key)
        self.create_buttons()

    def create_labels(self, key):
        """
        Crée les étiquettes pour le widget.

        Args:
            key: Clé utilisée pour identifier le générateur.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_spin_box("setpoint", initial_value=0, max_value=self.parent.config.get_constant_value(self.key), unit="V", function=self.update_AO)
        self.create_label("source_power", value="0")
        self.create_label("voltage_reflected", value="0")

    def create_buttons(self):
        """
        Crée les boutons pour le widget.
        """
        self.create_button("interlock_state", function=self.click_interlock, state="off")
        self.create_button("set_state", function=self.click_on_off, state="disabled")
        self.create_button("config", function=self.config)

    def interlock(self, new_state=None):
        """
        Définit l'état de l'interlock du générateur.

        Args:
            new_state: Nouvel état de l'interlock (facultatif).
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.interlock_state = new_state
            else:
                self.interlock_state = not self.interlock_state
            self.serial_reader.write_data(self.cmd.Interlock, self.interlock_state)
            self.update_button("interlock_state", state="on" if self.interlock_state else "off")

    def click_interlock(self):
        """
        Gère l'événement de clic pour le bouton de l'interlock.
        """
        self.interlock()

    def on_off(self, new_state=None):
        """
        Allume ou éteint le générateur.

        Args:
            new_state: Nouvel état du générateur (facultatif).
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state
            self.serial_reader.write_data(self.cmd.Enable, not self.state)
            self.update_button("set_state", state="enabled" if self.state else "disabled")

    def click_on_off(self):
        """
        Gère l'événement de clic pour le bouton marche/arrêt.
        """
        self.on_off()

    def config(self):
        """
        Ouvre la fenêtre de configuration pour le générateur.
        """
        pass

    def update_AI(self, value):
        """
        Met à jour la valeur AI du générateur.

        Args:
            value: Nouvelle valeur AI.
        """
        self.source_value = (float(value[0]) / 10 * self.parent.config.get_constant_value(self.key))
        self.voltage_reflected = (float(value[1]) / 10 * self.parent.config.get_constant_value(self.key))
        self.update_label("source_power", value=self.source_value)
        self.update_label("voltage_reflected", value=self.voltage_reflected)
        

    def update_AO(self, spin_box):
        """
        Updates the value of the label.
        """
        value = spin_box.value()/self.parent.config.get_constant_value(self.key)*10 #transform value to 0-10V
        self.parent.serial_reader.send_data(self.cmd.AO, value)  
        Logger.debug(f"{self.key} setpoint changed to {spin_box.value()}")

    def update_offset(self, spin_box):
        """
        Updates the value of the label.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()

    def set_value(self, value):
        '''
        Sets the value of the MFC. Used in recipes
        '''
        #change value of spinbox
        for spin_box, spin_box_key, _, spin_box_kwargs in self.spin_boxes:
            if spin_box_key == "setpoint":
                spin_box.setValue(value)
                self.update_AO(spin_box)
                break

    def get_value(self):
        '''
        Gets the value of the MFC. Used in recipes
        '''
        return self.source_value
    
    