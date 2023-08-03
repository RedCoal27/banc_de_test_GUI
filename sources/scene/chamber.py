from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class Chamber(CustomWidget):
    def __init__(self, pos , parent):
        ratio = (0.4, 0.2)
        super().__init__(parent.translator, pos, ratio, "#00B0F0", font_size=12)
        self.create_label("chamber", alignment = Qt.AlignmentFlag.AlignCenter)

        
    def set_font_size(self,size):
        self.font_size = size + 2

    
