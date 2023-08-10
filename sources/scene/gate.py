from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from scene.circle import Circle
from scene.line import Line
from internal.logger import Logger

class Gate():
    """
    Cette classe représente une porte dans une interface graphique.

    Methods:
        __init__(self, pos, relative_pos, key, cmd, sens, parent, color="#4472C4"):
            Initialise un objet Gate avec les paramètres donnés.
        
        on_left_click(self):
            Méthode appelée lorsqu'on clique sur la porte. Bascule l'état de la porte et met à jour la ligne connectant le cercle à la porte.
        
        change_state(self, new_state=None):
            Change l'état de la porte et met à jour la ligne connectant le cercle à la porte.
        
        set_value(self, value):
            Définit l'état de la porte. Utilisé pour les recettes.
    """

    def __init__(self, pos: tuple[float, float], relative_pos: tuple[float, float], key: str, cmd: int, sens: str, parent, color="#4472C4"):
        """
        Initialise un objet Gate avec les paramètres donnés.

        Args:
            pos: Tuple représentant la position de la porte dans la scène.
            relative_pos: Tuple représentant la position relative pour l'étiquette.
            key: Chaîne représentant la clé de la porte.
            cmd: Entier représentant la commande à envoyer au port série.
            sens: Chaîne représentant l'orientation de la porte ('horizontal' ou 'vertical').
            parent: Fenêtre principale de l'application.
            color: Couleur de la porte (par défaut : "#4472C4").

        Attributes:
            ratio: Liste représentant le rapport de la taille de la porte par rapport à la taille de son widget parent.
            pos: Tuple représentant la position de la porte dans la scène.
            relative_pos: Tuple représentant la position relative de la porte dans son widget parent.
            scene: Objet QGraphicsScene représentant la scène dans laquelle la porte sera affichée.
            sens: Chaîne représentant l'orientation de la porte ('horizontal' ou 'vertical').
            key: Chaîne représentant la clé de la porte.
            state: Booléen représentant l'état de la porte (ouverte ou fermée).
            cmd: Entier représentant la commande à envoyer au port série.
            parent: Fenêtre principale de l'application.
            text: Objet CustomWidget représentant l'étiquette textuelle de la porte.
            circle: Objet Circle représentant le cercle à côté de l'étiquette textuelle.
            line: Objet Line représentant la ligne connectant le cercle à la porte (horizontale ou verticale).
        """
        self.ratio = (0.05, 0.035)
        self.pos = pos
        self.relative_pos = relative_pos
        self.scene = parent.scene
        self.sens = sens
        self.key = key
        self.state = False
        self.cmd = cmd
        self.parent = parent

        # Ajout de l'étiquette textuelle
        self.text = CustomWidget(parent.translator, (pos[0] + relative_pos[0] - self.ratio[0] / 2, pos[1] + relative_pos[1] - self.ratio[0] / 2), self.ratio, "#FFFFFF")
        self.text.create_label(key, color="#8FAADC", alignment=Qt.AlignmentFlag.AlignCenter)
        self.scene.addItem(self.text)

        # Ajout du cercle à côté du texte
        self.circle = Circle(pos[0], pos[1], 0.015, "#4472C4", self.on_left_click)
        self.scene.addItem(self.circle)

        # Dessine la ligne horizontale
        self.line = Line(0, 0, 0, 0, color)
        self.on_left_click()
        self.scene.addItem(self.line)

    def on_left_click(self):
        """
        Méthode appelée lorsqu'on clique sur la porte.

        Bascule l'état de la porte et met à jour la ligne connectant le cercle à la porte en conséquence.
        """
        if self.parent.serial_reader.ser is not None and self.parent.auto_mode is False:
            self.change_state()

    def change_state(self, new_state=None):
        """
        Change l'état de la porte et met à jour la ligne connectant le cercle à la porte en conséquence.

        Args:
            new_state: Booléen représentant le nouvel état de la porte. Si None, l'état est basculé.
        """
        if new_state is not None:
            self.state = new_state
        else:
            self.state = not self.state

        if self.sens == 'horizontal':
            test_value = self.state
        else:
            test_value = not self.state

        if test_value is False:
            # Dessine la ligne verticale
            self.line.set_line(self.scene, self.circle.center[0], self.circle.center[1] - self.circle.radius * 1.2, self.circle.center[0], self.circle.center[1] + self.circle.radius * 1.2)
        else:
            # Dessine la ligne horizontale
            self.line.set_line(self.scene, self.circle.center[0] - self.circle.radius, self.circle.center[1], self.circle.center[0] + self.circle.radius, self.circle.center[1])

        if isinstance(self.cmd, int):
            self.parent.serial_reader.write_data(self.cmd, self.state)
        else:
            self.parent.serial_reader.write_data(self.cmd.DO, self.state)

        Logger.debug(f"La porte {self.key} est définie sur {self.state}")

    def set_value(self, value):
        """
        Définit l'état de la porte. Utilisé pour les recettes.

        Args:
            value: Booléen représentant le nouvel état de la porte.
        """
        self.change_state(value)
