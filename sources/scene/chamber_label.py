from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class ChamberLabel(CustomWidget):
    def __init__(self, pos , parent):
        ratio = (0.05, 0.025)
        super().__init__(parent.translator, pos, ratio, "#00B0F0")
        self.parent = parent
        self.recipes = self.parent.recipes
        self.combo_items = self.recipes.recipes.keys()

        # Création d'un QLabel, d'un QComboBox et d'un QPushButton dans le CustomWidget
        self.create_label_with_combo_box_and_button("auto", self.combo_items, self.button_function, color="black", button_key="set_state",state="Start")

        # self.create_button("Faire le vide", alignment = Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def button_stop(self):
        self.update_button("set_state", state = "Start")
        for combo_box, key , _ in self.combo_boxes:
            combo_box.setDisabled(False)

    def button_function(self):
        for combo_box, key , _ in self.combo_boxes:
            print(key)
            if key == "auto":
                if self.recipes.is_running() is False:
                    combo_box.setDisabled(True)
                    self.recipes.execute_recipe(combo_box.currentText())
                    self.update_button("set_state", state = "Stop")          
                    break
                else:
                    self.recipes.request_timer_stop.emit()
                    self.button_stop()
                    continue

    
