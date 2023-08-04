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
        self.create_label_with_combo_box_and_button("auto", self.combo_items, self.button_function, color="black", button_text="Click me!")

        # self.create_button("Faire le vide", alignment = Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def button_function(self):
        for value, key , _ in self.combo_boxes:
            print(key)
            if key == "auto":
                self.recipes.execute_recipe(value.currentText())
                break


    
    
