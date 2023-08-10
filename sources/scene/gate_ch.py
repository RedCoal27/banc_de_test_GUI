from scene.gate import *
from window.graph_window import GraphWindow
from PyQt5.QtWidgets import QMenu, QAction
import math

class GateCH(Gate):
    def __init__(self, pos: tuple[float,float], relative_pos: tuple[float,float], name: str, cmd: int, sens: str, parent, color="#4472C4"):
        super().__init__(pos, relative_pos, name, cmd, sens, parent, color)
        self.translator = parent.translator
        self.serial_reader = parent.serial_reader
        self.circle.setRightClickFunction(self.on_right_click)

        # Initialize sensor states and sensor line
        self.sensor_open = True
        self.sensor_close = True
        self.sensor_line = Line(0, 0, 0, 0, "#00FF00", 7)  # Using red for sensor line and a width of 7
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


    def update_DO(self, state):
        """
        Updates the DO label of the gate.

        Args:
        state: a boolean representing the state of the gate
        """
        self.change_state(state)

    def update_sensors(self, sensor_open, sensor_close):
        """
        Updates the sensor state of the gate.

        Args:
        sensor_open: a boolean representing the state of the upper sensor
        sensor_close: a boolean representing the state of the lower sensor
        """
        self.sensor_open = sensor_open
        self.sensor_close = sensor_close

    def update_sensor_line(self):
        """
        Updates the sensor line according to the sensor state of the gate.
        """
        offset = 0.0015 # Offset to compensate for the width of the line
        diag_length = (self.circle.radius) * math.sqrt(2)  # Calculate the length of the diagonal
        if self.sensor_open and not self.sensor_close:
            # Draw vertical line
            self.sensor_line.set_line(self.scene, self.circle.center[0]-self.circle.radius+offset, self.circle.center[1], self.circle.center[0]+self.circle.radius-offset, self.circle.center[1])
        elif self.sensor_close and not self.sensor_open:
            # Draw horizontal line
            self.sensor_line.set_line(self.scene, self.circle.center[0], self.circle.center[1]-self.circle.radius+offset, self.circle.center[0], self.circle.center[1]+self.circle.radius-offset)
        elif self.sensor_open and self.sensor_close or not self.sensor_open and not self.sensor_close:
            # Draw diagonal line
            self.sensor_line.set_line(self.scene, self.circle.center[0]-diag_length/2, self.circle.center[1]-diag_length/2, self.circle.center[0]+diag_length/2, self.circle.center[1]+diag_length/2)
        else:
            self.sensor_line.hide()



    def on_right_click(self, event):
        contextMenu = QMenu()

        sensorUpAction = QAction(self.translator.translate("sensor_open", state= 'off' if self.sensor_open else 'on'))
        sensorUpAction.setEnabled(False)  # Make it non-clickable
        contextMenu.addAction(sensorUpAction)

        sensorDownAction = QAction(self.translator.translate("sensor_close", state= 'off' if self.sensor_close else 'on'))
        sensorDownAction.setEnabled(False)  # Make it non-clickable
        contextMenu.addAction(sensorDownAction)


        cycleAction = QAction(self.translator.translate("change_state"))
        if self.parent.auto_mode is True:
            cycleAction.setEnabled(False)
        cycleAction.triggered.connect(self.on_left_click)
        contextMenu.addAction(cycleAction)

        changeStateAction = QAction(self.translator.translate("cycle"))
        if self.parent.auto_mode is True:
            changeStateAction.setEnabled(False)
        changeStateAction.triggered.connect(self.open_windows)
        contextMenu.addAction(changeStateAction)

        # Show the context menu.
        contextMenu.exec_(event.screenPos())


    def open_windows(self):
        self.window = GraphWindow(self, state_up_key="opening", state_down_key="closing")
        self.window.show()

    def get_value(self):
        """
        Gets the value of the gate. Used for recipes.
        
        """
        state = -1 if self.sensor_open*2 == self.sensor_close else 0 if not self.sensor_open else 1
        return state