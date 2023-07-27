from typing import Any
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QSpinBox, QPushButton, QGridLayout

class ConstantDialog(QDialog):
    def __init__(self, constants, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Constantes')

        self.layout = QGridLayout()
        self.spin_boxes = {}

        row = 0
        for i, (const, value) in enumerate(constants.items()):
            row = i // 5
            col = i % 5

            label = QLabel(const)
            spin_box = QSpinBox()
            spin_box.setValue(value)

            self.layout.addWidget(label, row, col*2)
            self.layout.addWidget(spin_box, row, col*2 + 1)
            self.spin_boxes[const] = spin_box

        self.confirm_button = QPushButton('Confirmer')
        self.confirm_button.clicked.connect(self.confirm)
        self.layout.addWidget(self.confirm_button, row + 1, 0, 1, 10)

        self.setLayout(self.layout)

    def confirm(self):
        new_constants = {const: spin_box.value() for const, spin_box in self.spin_boxes.items()}
        # Ici, vous pouvez enregistrer les nouvelles constantes où vous voulez
        # ...
        self.close()




MCP2_A = 1
MCP2_B = 2
MCP3_A = 3
MCP3_B = 4

class Cmd():
    nupro_final = 3
    nupro_mfc1 = 1
    nupro_mfc2 = 2
    nupro_vent = 4

    turbo_pump_rga_gate = 16
    turbo_pump_rga_gate_p = 17

    turbo_pump_ch_gate = 5 
    turbo_pump_ch_gate_p = 15

    iso_chamber = 14

    RoughingPump = 26
    TurboRGA = 27
    TurboCH = 28

    MFC1 = 2
    MFC2 = 3

    class WL1():
        DO = 10
        Port = MCP2_A #input port
        Up = 64
        Down = 128

    class WL2():
        DO = 9
        Port = MCP2_A #input port
        Up = 16
        Down = 32

    class WL3():
        DO = 8
        Port = MCP2_A #input port
        Up = 4
        Down = 8

    class SV():
        DO = 7
        Port = MCP2_A #input port
        Up = 1
        Down = 2

    class RGAGate():
        DO = 16
        Port = MCP2_B #input port
        Up = 1 #Open
        Down = 2 #Close

        


class PiraniConfig():
    gas_types = ["N2", "Ar", "He", "CO2", "H", "Ne", "Kr"]
    units_types = ["mBar", "Pascal", "Torr"]

        
