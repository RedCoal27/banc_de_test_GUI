from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class Label(CustomWidget):
    def __init__(self, pos, ratio , key , parent):
        super().__init__(parent.translator, pos, ratio, "#FFFFFF")
        self.create_label(key, color="#8FAADC", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.scene = parent.scene
        self.scene.addItem(self)





