from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class Auto(CustomWidget):
    def __init__(self, pos , parent):
        ratio = (0.1, 0.05)
        self.parent = parent
        self.parent.auto_mode = False
        super().__init__(parent.translator, pos, ratio, "#FFD966")

        self.layout.setContentsMargins(8, 8, 8, 8)  # Add this line to remove margins

        self.create_button("set_state", function=self.auto, state = "manual")

    def auto(self):
        if self.parent.auto_mode is True:
            self.set_manual()
        else:
            self.set_auto()
    
    def set_auto(self):
        self.parent.auto_mode = True
        self.parent.custom_widgets["chamber_label"].show()
        for custom_widget in self.parent.custom_widgets.values():
            if isinstance(custom_widget, CustomWidget):
                for button in custom_widget.buttons:
                    button[0].setEnabled(False)
                for spin_box in custom_widget.spin_boxes:
                    spin_box[0].setEnabled(False)

        self.update_button("set_state", state = "auto")
        self.buttons[0][0].setEnabled(True)
        self.parent.custom_widgets["chamber_label"].buttons[0][0].setEnabled(True)

    def set_manual(self):
        self.parent.auto_mode = False
        self.parent.custom_widgets["chamber_label"].hide()
        for custom_widget in self.parent.custom_widgets.values():
            if isinstance(custom_widget, CustomWidget):
                for button in custom_widget.buttons:
                    button[0].setEnabled(True)
                for spin_box in custom_widget.spin_boxes:
                    spin_box[0].setEnabled(True)

        self.update_button("set_state", state = "manual")