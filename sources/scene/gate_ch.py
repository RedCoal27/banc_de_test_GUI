from scene.gate import *
from graph_window import GraphWindow
import math

class GateCH(Gate):
    def __init__(self, pos: tuple[float,float], relative_pos: tuple[float,float], name: str, cmd: int, sens: str, parent):
        super().__init__(pos, relative_pos, name, cmd, sens, parent)
        self.translator = parent.translator
        self.serial_reader = parent.serial_reader
        self.circle.setRightClickFunction(self.open_windows)

        # Initialize sensor states and sensor line
        self.sensor_up = False
        self.sensor_down = True
        self.sensor_line = Line(0, 0, 0, 0, "#FF0000", 5)  # Using red for sensor line and a width of 2
        # Remove the original line from the scene and re-add it to make sure it's on top
        self.scene.removeItem(self.line)
        self.scene.addItem(self.sensor_line)
        self.scene.addItem(self.line)

        self.update_sensor_line()

    def on_left_click(self):
        """
        A method called when the gate is clicked.

        Toggles the state of the gate and updates the line connecting the circle to the gate accordingly.
        """
        super().on_left_click()

    def open_windows(self):
        self.window = GraphWindow(self)
        self.window.show()

    def update_DO(self, state):
        """
        Updates the DO label of the gate.

        Args:
        - state: a boolean representing the state of the gate
        """
        self.change_state(state)

    def update_sensors(self, sensor_up, sensor_down):
        """
        Updates the sensor state of the gate.

        Args:
        - sensor_up: a boolean representing the state of the upper sensor
        - sensor_down: a boolean representing the state of the lower sensor
        """
        self.sensor_up = sensor_up
        self.sensor_down = sensor_down
        self.update_sensor_line()

    def update_sensor_line(self):
        """
        Updates the sensor line according to the sensor state of the gate.
        """
        offset = 0.0015 # Offset to compensate for the width of the line
        diag_length = (self.circle.radius) * math.sqrt(2)  # Calculate the length of the diagonal

        if self.sensor_up and not self.sensor_down:
            # Draw vertical line
            self.sensor_line.set_line(self.scene, self.circle.center[0], self.circle.center[1]-self.circle.radius+offset, self.circle.center[0], self.circle.center[1]+self.circle.radius-offset)
        elif self.sensor_down and not self.sensor_up:
            # Draw horizontal line
            self.sensor_line.set_line(self.scene, self.circle.center[0]-self.circle.radius+offset, self.circle.center[1], self.circle.center[0]+self.circle.radius-offset, self.circle.center[1])
        elif self.sensor_up == self.sensor_down:
            # Draw diagonal line
            self.sensor_line.set_line(self.scene, self.circle.center[0]-diag_length/2, self.circle.center[1]-diag_length/2, self.circle.center[0]+diag_length/2, self.circle.center[1]+diag_length/2)
        else:
            self.sensor_line.hide()
