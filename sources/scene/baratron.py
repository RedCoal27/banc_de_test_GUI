from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

# Baratron Widget: Represents a UI component related to a Baratron.
class Baratron(CustomWidget):
    '''Initializes the Baratron widget.
    
    Args:
    pos: Position for the widget.
    key: Key associated with the widget.
    parent: Parent for the widget.
    '''
    def __init__(self, pos, key, parent):
        ratio = (0.12, 0.1)
        self.offset = 0
        self.key = key
        self.value = 0
        super().__init__(parent.translator, pos, ratio, "#C5E0B4")
        self.create_labels(key)

    '''Creates labels for the Baratron widget.
    
    Args:
    key: a string representing the key of the widget.
    '''
    def create_labels(self, key):
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label("pressure", value="0", unit=" Torr")
        self.create_label_with_spin_box("offset", unit=" Torr", initial_value=0, min_value=-100, max_value=100, function=self.update_offset)
        self.create_label("size", value="0.1", unit=" Torr")

    '''Updates the value of the Baratron's label with specific logic.
    
    Args:
    value: The value to be updated in the label.
    '''
    def update_AI(self, value):
        unit = " Torr"
        value = float(value)
        if value > 10.5:
            value = "overrange"
            unit = ""
        else:
            value = value*0.1/10 - self.offset
            value = f"{value:.2e}"  # Scientific notation with 1 decimal
            base, exp = value.split("e")
            if len(exp) == 3:
                exp = exp[0] + exp[2]
            value = base + "E" + exp
        self.value = value
        self.update_label("pressure", value=value, unit=unit)

    '''Updates the offset value for the Baratron.
    
    Args:
    spin_box: The spin box widget that provides the offset value.
    '''
    def update_offset(self, spin_box):
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()


    def get_value(self):
        '''Returns the current value of the Baratron.
        Returns:
        float: The current value, with specific handling for "overrange".
        '''
        if self.value == "overrange":
            return 1000
        else:
            return float(self.value)