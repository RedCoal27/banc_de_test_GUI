from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from window.throttle_valve_gui import ThrottleValveGUI
from internal.constant import Cmd


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
        ratio = (0.12, 0.25)
        self.parent = parent
        self.serial_reader = parent.serial_reader
        super().__init__(parent.translator, pos, ratio, "#F8CBAD")
        self.create_labels(key)
        self.create_buttons()
        self.state = 1
        self.step = 0

        self.window = ThrottleValveGUI(self)


    def create_labels(self, key):
        """
        Crée des étiquettes pour le widget ThrottleValve.

        Args:
            key: Clé utilisée pour identifier la vanne.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("di_open", state="false")
        self.create_label("di_close", state="false")
        self.create_label("steps", value="")
        self.create_label_with_spin_box("close_position", state="false", min=0, max=100, step=1, value=0)
        self.create_label_with_spin_box("hysteresis", state="false", min=0, max=100, step=1, value=0)

    def create_buttons(self):
        """
        Crée des boutons pour le widget ThrottleValve.
        """
        self.create_button("set_state", state="", function=self.click_DO)
        self.create_button("routine", function=self.open_window)
        # self.create_button("cycle", state="false")


    def set_position(self, value):
        self.serial_reader.send_data(Cmd.ThrottleValve.cmd, Cmd.ThrottleValve.set_position, value.to_bytes(2, byteorder='little', signed=True))


    def update_DO(self, new_state=None):
        """
        Met à jour les étiquettes DO du widget FourWay.
        """
        if self.serial_reader.ser is not None and not self.window.isVisible():
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state
            new_pos = 800
            if(self.state):
                new_pos = 0
                
            self.set_position(new_pos)
            self.update_button("set_state", state="close" if self.state else "open")

    def click_DO(self):
        """
        Fonction de rappel pour le bouton set_state. Met à jour les étiquettes DO du widget FourWay.
        """
        self.update_DO()


    def update_sensor(self, data):
        """
        Met à jour les étiquettes DI du widget FourWay.

        Args:
            up: Booléen représentant l'état du DI supérieur.
            down: Booléen représentant l'état du DI inférieur.
        """
        self.sensor_open = data & 2
        self.sensor_close = data & 1
        self.update_label('di_open', state="true" if self.sensor_open else "false")
        self.update_label('di_close', state="true" if self.sensor_close else "false")

    def update_position(self,pos):
        self.step = pos
        self.update_label("steps", value =  pos)

    def open_window(self):
        """
        Ouvre une fenêtre pour configurer la vanne.
        """
        self.window.setWindowModality(Qt.ApplicationModal)  # Rend la fenêtre modale
        self.window.show()
        self.window.raise_()

