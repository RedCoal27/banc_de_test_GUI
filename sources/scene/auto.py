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
        self.parent.auto_mode = not self.parent.auto_mode
        if self.parent.auto_mode is True:
            self.update_button("set_state", state = "auto")
            self.parent.custom_widgets["chamber_label"].show()
        else:
            self.update_button("set_state", state = "manual")
            self.parent.custom_widgets["chamber_label"].hide()

    
