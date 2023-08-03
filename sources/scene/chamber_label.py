from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class ChamberLabel(CustomWidget):
    def __init__(self, pos , parent):
        ratio = (0.1, 0.05)
        super().__init__(parent.translator, pos, ratio, "#00B0F0")
        self.create_label("cmd", alignment = Qt.AlignmentFlag.AlignLeft, state="manual")
        # self.create_button("Faire le vide", alignment = Qt.AlignmentFlag.AlignCenter)


        
    def set_font_size(self,size):
        self.font_size = size

    
