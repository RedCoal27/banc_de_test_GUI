from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class Auto(CustomWidget):
    """
    La classe Auto gère la fonctionnalité du mode automatique au sein d'un widget parent. Elle hérite de la classe CustomWidget.

    Attributes:
        parent: Référence au widget parent contenant ce widget Auto.

    Methods:
        __init__(self, pos, parent):
            Initialise le widget Auto avec la position et le widget parent spécifiés. Configure les attributs et crée le bouton basculant.

        auto(self):
            Bascule entre les modes automatique et manuel.

        set_auto(self):
            Définit le widget en mode automatique et met à jour les composants associés.

        set_manual(self):
            Définit le widget en mode manuel et met à jour les composants associés.
    
    Components:
        buttons (list): 
            self.buttons[0] (list): Liste contenant le bouton basculant entre les modes automatique et manuel.
    """

    def __init__(self, pos, parent):
        """
        Initialise le widget Auto avec la position et le widget parent spécifiés. Configure les attributs et crée le bouton basculant.

        Args:
            pos (tuple): Position du widget dans le parent.
            parent (QWidget): Référence au widget parent contenant ce widget Auto.
        """
        ratio = (0.1, 0.05)
        self.parent = parent
        self.parent.auto_mode = False
        super().__init__(parent.translator, pos, ratio, "#FFD966")
        self.layout.setContentsMargins(8, 8, 8, 8)  # Ajouter cette ligne pour supprimer les marges
        self.create_button("set_state", function=self.auto, state="manual")

    def auto(self):
        """
        Bascule entre les modes automatique et manuel.
        """
        if self.parent.auto_mode is True:
            self.set_manual()
        else:
            self.set_auto()

    def set_auto(self):
        """
        Définit le widget en mode automatique et met à jour les composants associés.
        """
        self.parent.auto_mode = True
        self.parent.custom_widgets["chamber_label"].show()
        for custom_widget in self.parent.custom_widgets.values():
            if isinstance(custom_widget, CustomWidget):
                for button in custom_widget.buttons:
                    button[0].setEnabled(False)
                for spin_box in custom_widget.spin_boxes:
                    spin_box[0].setEnabled(False)

        self.update_button("set_state", state="auto")
        self.buttons[0][0].setEnabled(True)
        self.parent.custom_widgets["chamber_label"].buttons[0][0].setEnabled(True)

    def set_manual(self):
        """
        Définit le widget en mode manuel et met à jour les composants associés.
        """
        self.parent.auto_mode = False
        self.parent.custom_widgets["chamber_label"].hide()
        for custom_widget in self.parent.custom_widgets.values():
            if isinstance(custom_widget, CustomWidget):
                for button in custom_widget.buttons:
                    button[0].setEnabled(True)
                for spin_box in custom_widget.spin_boxes:
                    spin_box[0].setEnabled(True)

        self.update_button("set_state", state="manual")
