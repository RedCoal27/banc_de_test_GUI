from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget

class ChamberLabel(CustomWidget):
    """
    La classe ChamberLabel gère l'étiquetage et les contrôles à l'intérieur d'une chambre. Elle hérite de la classe CustomWidget.

    Attributes:
        parent: Référence au widget parent contenant ce widget ChamberLabel.
        recipes: Référence à la classe recipes associée au parent.
        combo_items: Clés des recettes à utiliser dans la boîte de sélection.

    Methods:
        __init__(self, pos, parent):
            Initialise le widget ChamberLabel avec la position et le parent donnés. Configure les attributs et crée des étiquettes, des boîtes de sélection et des boutons.

        button_stop(self):
            Gère la fonctionnalité du bouton d'arrêt et met à jour les composants associés.

        button_function(self):
            Gère la fonctionnalité du bouton pour l'étiquette de la chambre, y compris le démarrage et l'arrêt des recettes.

        update_step(self, name, step, total_steps):
            Met à jour l'étiquette de l'étape avec les valeurs données.

        update_time(self, type, time):
            Met à jour la valeur de l'étiquette de temps.
        
    Components: 
        labels: Un dictionnaire d'étiquettes associées au widget ChamberLabel.
            recipes: QLabel affichant le texte "Recettes".
            step: QLabel affichant le nom de l'étape, le numéro de l'étape actuelle et le nombre total d'étapes.
            time_display: QLabel affichant le temps restant ou le temps écoulé.
        combo_boxes: Un dictionnaire de QComboBox associé au widget ChamberLabel.
            recipes: QComboBox contenant les recettes disponibles.
        buttons: Un dictionnaire de QPushButton associé au widget ChamberLabel.
            set_state: QPushButton qui démarre ou arrête la recette.
    """
    def __init__(self, pos, parent):
        """
        Initialise le widget ChamberLabel avec la position et le parent spécifiés. Configure les attributs et crée des étiquettes, des boîtes de sélection et des boutons.

        Args:
            pos: Position du widget dans le parent.
            parent: Référence au widget parent contenant ce widget ChamberLabel.
        """
        ratio = (0.05, 0.025)
        super().__init__(parent.translator, pos, ratio, "#00B0F0")
        self.parent = parent
        self.recipes = self.parent.recipes
        self.combo_items = self.recipes.recipes.keys()

        # Création de QLabel, QComboBox et QPushButton dans le CustomWidget
        self.create_label_with_combo_box_and_button("recipes", self.combo_items, self.button_function, button_key="set_state", state="Start")
        self.create_label("step", name="", step="", total_steps="")
        self.create_label("time_display", type="")

        # self.create_button("Faire le vide", alignment = Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def button_stop(self):
        """
        Gère la fonctionnalité du bouton d'arrêt et met à jour les composants associés.
        """
        self.update_button("set_state", state="Start")
        for combo_box, key, _ in self.combo_boxes:
            combo_box.setDisabled(False)
            self.parent.custom_widgets["auto"].buttons[0][0].setDisabled(False)

    def button_function(self):
        """
        Gère la fonctionnalité du bouton pour l'étiquette de la chambre, y compris le démarrage et l'arrêt des recettes.
        """
        for combo_box, key, _ in self.combo_boxes:
            if key == "recipes":
                if self.recipes.is_running() is False:
                    combo_box.setDisabled(True)
                    self.recipes.execute_recipe(combo_box.currentText())
                    self.update_button("set_state", state="Stop")
                    self.parent.custom_widgets["auto"].buttons[0][0].setDisabled(True)
                    break
                else:
                    self.recipes.request_timer_stop.emit()
                    self.button_stop()
                    continue

    def update_step(self, name, step, total_steps):
        """
        Met à jour l'étiquette de l'étape avec les valeurs données.

        Args:
            name: Nom de l'étape.
            step: Numéro de l'étape actuelle.
            total_steps: Nombre total d'étapes.
        """
        self.update_label("step", name=name, step=step, total_steps=total_steps)

    def update_time(self, type, time):
        """
        Met à jour la valeur de l'étiquette de temps.

        Args:
            type: Type de mise à jour du temps ; peut être 'time_left' ou 'timeout'.
            time: Valeur du temps à mettre à jour.
        """
        self.update_label("time_display", type=self.translator.translate(type, value=time))
