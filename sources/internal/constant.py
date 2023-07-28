from typing import Any
from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

class ConstantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)


        self.setWindowTitle('Constantes')


        self.parent = parent
        constants = self.parent.config["constant"]

        self.layout = QGridLayout()
        self.spin_boxes = {}

        for i, (category, consts) in enumerate(constants.items()):
            label = QLabel(self.parent.translator.translate(category))
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label, 0, i*2, 1, 2)

            for j, (const, value) in enumerate(consts.items()):
                const_label = QLabel(self.parent.translator.translate(const))
                const_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                spin_box = QSpinBox()
                spin_box.setValue(value)

                self.layout.addWidget(const_label, j + 1, i*2)
                self.layout.addWidget(spin_box, j + 1, i*2 + 1)
                self.spin_boxes[(category, const)] = spin_box


        self.confirm_button = QPushButton('Confirmer')
        self.confirm_button.clicked.connect(self.confirm)
        self.layout.addWidget(self.confirm_button, len(max(constants.values(), key=len)) + 1, 0, 1, i*2 + 2)

        self.setLayout(self.layout)
        self.setFixedSize(self.layout.sizeHint())

    def confirm(self):
        self.parent().config["constant"] = {(category, const): spin_box.value() for (category, const), spin_box in self.spin_boxes.items()}
        self.parent().config.save_config()



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
        DO = 6 #CVD
        Port = MCP2_B #input port
        Up = 4 #Open
        Down = 8 #Close

    class Interlock():
        Port = MCP3_A
        RoughingPumpOff = 1
        PumpPressureHigh = 2
        ChamberOpen = 4
        ChamberPressureHigh = 8


        


class PiraniConfig():
    gas_types = ["N2", "Ar", "He", "CO2", "H", "Ne", "Kr"]
    units_types = ["mBar", "Pascal", "Torr"]

        
