"""
This module contains the Generator class, a custom widget for controlling a generator.

Attributes:
- serial_reader: The serial reader object used for communication with the generator.
- key: The key used to identify the generator.
- cmd: The command object used for sending commands to the generator.
- state: The current state of the generator (on/off).
- interlock_state: The current state of the interlock (on/off).
- source_value: The current source value of the generator.
- voltage_reflected: The current reflected voltage of the generator.
- parent: The parent object of the widget.

Methods:
- __init__(self, pos, cmd, key , parent): Initializes the Generator object.
- create_labels(self,key): Creates the labels for the widget.
- create_buttons(self): Creates the buttons for the widget.
- interlock(self, new_state=None): Sets the interlock state of the generator.
- click_interlock(self): Handles the click event for the interlock button.
- on_off(self, new_state=None): Turns the generator on or off.
- click_on_off(self): Handles the click event for the on/off button.
- config(self): Opens the configuration dialog for the generator.
- update_AI(self, value): Updates the AI value of the generator.
- update_AO(self, spin_box): Updates the AO value of the generator.
- update_offset(self, spin_box): Updates the offset value of the generator.
- set_value(self, value): Sets the value of the generator.
"""
from PyQt5.QtCore import Qt
from internal.custom_widget import CustomWidget
from internal.logger import Logger

class Generator(CustomWidget):
    """
    A custom widget for controlling a generator.

    Attributes:
    - serial_reader: The serial reader object used for communication with the generator.
    - key: The key used to identify the generator.
    - cmd: The command object used for sending commands to the generator.
    - state: The current state of the generator (on/off).
    - interlock_state: The current state of the interlock (on/off).
    - source_value: The current source value of the generator.
    - voltage_reflected: The current reflected voltage of the generator.
    - parent: The parent object of the widget.
    """

    def __init__(self, pos, cmd, key , parent):
        """
        Initializes the Generator object.

        Args:
        - pos: The position of the widget.
        - cmd: The command object used for sending commands to the generator.
        - key: The key used to identify the generator.
        - parent: The parent object of the widget.
        """
        ratio = (0.1, 0.15)
        self.serial_reader = parent.serial_reader
        self.key = key
        self.cmd = cmd
        self.state = False
        self.interlock_state = False
        self.source_value = 0
        self.voltage_reflected = 0
        self.parent = parent
        super().__init__(parent.translator, pos, ratio, "#B4C7E7")
        self.create_labels(key)
        self.create_buttons()

    def create_labels(self,key):
        """
        Creates the labels for the widget.

        Args:
        - key: The key used to identify the generator.
        """
        self.create_label(key, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.create_label_with_spin_box("setpoint", initial_value=0, max_value=self.parent.config.get_constant_value(self.key), unit="V", function=self.update_AO)
        self.create_label("source_power", value = "0", unit = "W")
        self.create_label("voltage_reflected", value = "0", unit = "V ou W")

    def create_buttons(self):
        """
        Creates the buttons for the widget.
        """
        self.create_button("interlock_state", function=self.click_interlock, state="off")
        self.create_button("set_state", function=self.click_on_off, state="disabled")
        self.create_button("Config", function=self.config)

    def interlock(self, new_state=None):
        """
        Sets the interlock state of the generator.

        Args:
        - new_state: The new state of the interlock (optional).
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.interlock_state = new_state
            else:
                self.interlock_state = not self.interlock_state
            self.serial_reader.write_data(self.cmd.Interlock, self.interlock_state)
            self.update_button("interlock_state", state = "on" if self.interlock_state else "off")

    def click_interlock(self):
        """
        Handles the click event for the interlock button.
        """
        self.interlock()

    def on_off(self, new_state=None):
        """
        Turns the generator on or off.

        Args:
        - new_state: The new state of the generator (optional).
        """
        if self.serial_reader.ser is not None:
            if new_state is not None:
                self.state = new_state
            else:
                self.state = not self.state
            self.serial_reader.write_data(self.cmd.Enable, not self.state)
            self.update_button("set_state", state = "enabled" if self.state else "disabled")

    def click_on_off(self):
        """
        Handles the click event for the on/off button.
        """
        self.on_off()

    def config(self):
        """
        Opens the configuration dialog for the generator.
        """
        pass

    def update_AI(self, value):
        """
        Updates the AI value of the generator.

        Args:
        - value: The new AI value.
        """
        self.source_value = (float(value[0])/10*self.parent.config.get_constant_value(self.key))
        self.voltage_reflected = (float(value[1])/10*self.parent.config.get_constant_value(self.key))
        self.update_label("source_power", value = self.source_value, unit = "W")
        self.update_label("voltage_reflected", value = self.voltage_reflected, unit = "V ou W")

    def update_AO(self, spin_box):
        """
        Updates the AO value of the generator.

        Args:
        - spin_box: The spin box object containing the new AO value.
        """
        value = spin_box.value()/self.parent.config.get_constant_value(self.key)*10 #transform value to 0-10V
        self.parent.serial_reader.send_data(self.cmd.AO, value)  
        Logger.debug(f"{self.key} setpoint changed to {spin_box.value()}")

    def update_offset(self, spin_box):
        """
        Updates the offset value of the generator.

        Args:
        - spin_box: The spin box object containing the new offset value.
        """
        Logger.debug(f"{self.key} offset changed to {spin_box.value()}")
        self.offset = spin_box.value()

    def set_value(self, value):
        """
        Sets the value of the generator.

        Args:
        - value: The new value.
        """
        for spin_box, spin_box_key, _, spin_box_kwargs in self.spin_boxes:
            if spin_box_key == "setpoint":
                spin_box.setValue(value)
                self.update_AO(spin_box)
                break

    def get_value(self):
        """
        Gets the current value of the generator.
        """
        return self.source_value
