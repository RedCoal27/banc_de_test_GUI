from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QPushButton, QGridLayout, QComboBox, QToolTip, QSizePolicy
from PyQt5.QtCore import Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)


class ConstantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setWindowTitle('Constantes')

        self.parent = parent
        constants = self.parent.config["constants"]

        self.layout = QGridLayout()

        self.spin_boxes = {}
        self.combo_boxes = {}

        max_rows = 0

        for i, constant in enumerate(constants):
            category = constant["name"]
            consts = constant["values"]

            label = QLabel(self.parent.translator.translate(category))
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label, 0, i*3, 1, 3)  # Change i*2 to i*3

            for j, (const, value) in enumerate(consts.items()):
                const_label = QLabel(self.parent.translator.translate(const))
                const_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                const_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

                max_rows = max(max_rows, len(consts))

                if isinstance(value, dict):
                    spin_box = QSpinBox()
                    
                    # Set the minimum and maximum values if they are defined in the JSON
                    if "min" in value:
                        spin_box.setMinimum(value["min"])
                    if "max" in value:
                        spin_box.setMaximum(value["max"])

                    spin_box.setValue(value["value"])
                    spin_box.setFixedWidth(60)  # Set a fixed width for the spin box



                    self.spin_boxes[(i, const)] = spin_box  # Change (category, const) to (i, const)
                    self.layout.addWidget(const_label, j + 1, i*3)  # Change i*2 to i*3
                    self.layout.addWidget(spin_box, j + 1, i*3 + 1)  # Change i*2 + 1 to i*3 + 1

                    unit_string = str(value["unit"])
                    unit_label = QLabel(unit_string)
                    unit_label.setMaximumWidth(50)  # Set a slightly larger fixed width for the unit label
                    unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.layout.addWidget(unit_label, j + 1, i*3 + 2)  # Change i*2 + 2 to i*3 + 2
                    
                    if "tooltip" in value:
                        const_label.setToolTip(self.parent.translator.translate(value["tooltip"]))
                        spin_box.setToolTip(self.parent.translator.translate(value["tooltip"]))
                else:
                    combo_box = QComboBox()
                    combo_box.addItems(value)
                    self.combo_boxes[(i, const)] = combo_box  # Change (category, const) to (i, const)
                    self.layout.addWidget(const_label, j + 1, i*3)  # Change i*2 to i*3
                    self.layout.addWidget(combo_box, j + 1, i*3 + 1)  # Change i*2 + 1 to i*3 + 1

        self.confirm_button = QPushButton('Confirmer')
        self.confirm_button.clicked.connect(self.confirm)
        self.confirm_button.setFixedWidth(100)

        self.layout.addWidget(self.confirm_button, max_rows + 1, 0, 1, i*3 + 2, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.setFixedSize(self.sizeHint())

    def confirm(self):
        for (index, const), spin_box in self.spin_boxes.items():
            self.parent.config["constants"][index]["values"][const]["value"] = spin_box.value()

        for (index, const), combo_box in self.combo_boxes.items():
            self.parent.config["constants"][index]["values"][const] = combo_box.currentText()

        self.parent.config.save_config()
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
        RoughingPumpOff = 2
        PumpPressureHigh = 8
        ChamberOpen = 1
        ChamberPressureHigh = 4


        


class PiraniConfig():
    gas_types = ["N2", "Ar", "He", "CO2", "H", "Ne", "Kr"]
    units_types = ["mBar", "Pascal", "Torr"]

        
