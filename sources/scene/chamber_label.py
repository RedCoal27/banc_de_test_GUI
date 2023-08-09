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
        self.create_label_with_combo_box_and_button("recipes", self.combo_items, self.button_function, color="black", button_key="set_state",state="Start")
        self.create_label("step", name = "", step = "", total_steps = "")
        self.create_label("time_display", type = "")


        # self.create_button("Faire le vide", alignment = Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def button_stop(self):
        self.update_button("set_state", state = "Start")
        for combo_box, key , _ in self.combo_boxes:
            combo_box.setDisabled(False)
            self.parent.custom_widgets["auto"].buttons[0][0].setDisabled(False)

    def button_function(self):
        for combo_box, key , _ in self.combo_boxes:
            if key == "recipes":
                if self.recipes.is_running() is False:
                    combo_box.setDisabled(True)
                    self.recipes.execute_recipe(combo_box.currentText())
                    self.update_button("set_state", state = "Stop")  
                    self.parent.custom_widgets["auto"].buttons[0][0].setDisabled(True)        
                    break
                else:
                    self.recipes.request_timer_stop.emit()
                    self.button_stop()
                    continue

    def update_step(self, name, step, total_steps):
        self.update_label("step", name = name, step = step, total_steps = total_steps)

    def update_time(self, type, time):
        '''
        Updates the value of the label.
        type can be:
        - time_left: time left before the next step
        - timeout: time left before the timeout
        '''
        self.update_label("time_display", type = self.translator.translate(type, value = time))