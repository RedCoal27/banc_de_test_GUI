from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

from custom_widget import CustomWidget
from circle import Circle
from line import Line

class Gate():
    def __init__(self, pos: tuple[float,float], relative_pos: tuple[float,float], name: str, cmd: str, sens: str, parent):
        """
        A class representing a gate in a graphical interface.

        Args:
        - pos: a tuple representing the position of the gate in the scene
        - relative_pos: a tuple representing the relative position for the label
        - name: a string representing the name of the gate
        - cmd: a string representing the command to be sent to the serial port
        - sens: a string representing the orientation of the gate ('horizontal' or 'vertical')
        - parent: the main window of the application

        Attributes:
        - ratio: a list representing the ratio of the gate's size to the size of its parent widget
        - pos: a tuple representing the position of the gate in the scene
        - relative_pos: a tuple representing the relative position of the gate within its parent widget
        - scene: a QGraphicsScene object representing the scene in which the gate will be displayed
        - sens: a string representing the orientation of the gate ('horizontal' or 'vertical')
        - text: a CustomWidget object representing the text label of the gate
        - circle: a Circle object representing the circle next to the text label
        - state: a boolean representing the state of the gate (open or closed)
        - line: a Line object representing the line connecting the circle to the gate (horizontal or vertical)
        """
        self.ratio = (0.05, 0.035)
        self.pos = pos
        self.relative_pos = relative_pos
        self.scene = parent.scene
        self.sens = sens
        self.name = name
        self.state = True
        self.cmd = cmd
        self.serial_reader = parent.serial_reader

        #add text label
        self.text = CustomWidget(parent.translator, (pos[0]+relative_pos[0]-self.ratio[0]/2,pos[1]+relative_pos[1]-self.ratio[0]/2), self.ratio, "#FFFFFF")
        self.text.create_label(name, color="#8FAADC", alignment = Qt.AlignCenter)
        self.scene.addItem(self.text)

        #add circle next to text
        self.circle = Circle(pos[0] , pos[1], 0.015, "#4472C4", self.on_click)
        self.scene.addItem(self.circle)
        


        #draw horizontal line
        self.line = Line(0,0,0,0, "#4472C4")
        self.on_click()
        self.scene.addItem(self.line)

    def on_click(self):
        """
        A method called when the gate is clicked.

        Toggles the state of the gate and updates the line connecting the circle to the gate accordingly.
        """
        if self.serial_reader.ser is not None:
            if self.sens == 'horizontal':
                test_value = self.state
            else:
                test_value = not self.state

            if test_value == False: 
                #draw vertical line
                self.line.set_line(self.scene,self.circle.center[0], self.circle.center[1]-self.circle.radius*1.2, self.circle.center[0], self.circle.center[1]+self.circle.radius*1.2)
            else:
                self.line.set_line(self.scene,self.circle.center[0]-self.circle.radius, self.circle.center[1], self.circle.center[0]+self.circle.radius, self.circle.center[1])
            self.state = not self.state

            self.serial_reader.write_data(self.cmd, not self.state)
            

        # print("self.state",self.state)