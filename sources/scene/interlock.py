from PyQt5.QtCore import Qt

from internal.custom_widget import CustomWidget

class Interlock(CustomWidget):
    def __init__(self, pos , key , parent):
        ratio = (0.15, 0.10)
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#FFD966")
        self.states = []
        self.create_labels(key)
        
    def create_labels(self,key):
        """
        Creates labels for the FourWay widget.

        Args:
        - key: a string representing the key of the widget
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_indicator("roughing_pump_state", state = "On")
        self.create_label_with_indicator("pump_pressure_high", sens = "<", value = self.parent.config["pump_pressure"]["setpoint_low"])
        self.create_label_with_indicator("chamber_open", state = "close")
        self.create_label_with_indicator("chamber_pressure_high", sens = "<", value = self.parent.config["chamber_pressure"]["setpoint_low"])

    def update_interlock(self, states):
        """
        Updates the labels of the FourWay widget.

        Args:
        - states: liste of booleans representing the state of the indicators
        """
        # states = [not state for state in states]
        self.states = states
        self.update_indicator(self, "roughing_pump_state", states[0])
        self.update_indicator(self, "pump_pressure_high", states[1])
        self.update_indicator(self, "chamber_open", states[2])
        self.update_indicator(self, "chamber_pressure_high", states[3])

        self.update_label("roughing_pump_state", state = "off" if states[0] else "on")
        self.update_label("pump_pressure_high", sens = ">" if states[0] else "<", value = self.parent.config["pump_pressure"]["setpoint_low"])
        self.update_label("chamber_open", state = "open" if states[0] else "close")
        self.update_label("chamber_pressure_high", sens = ">" if states[0] else "<", value = self.parent.config["chamber_pressure"]["setpoint_low"])

    def get_value(self):
        '''
        Returns the value of the widget. Used in the recipe.
        '''
        value = 0
        for i, state in enumerate(self.states):
            if state:
                value += 2**i
        return value