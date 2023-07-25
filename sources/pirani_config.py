from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QGridLayout, QDoubleSpinBox, QMessageBox, QSpinBox)

class NodeAddressWindow(QWidget):
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key
        super(NodeAddressWindow, self).__init__(None)
        self.setWindowTitle(self.parent.translator.translate("set_node_address"))

        layout = QVBoxLayout()
        self.address_spin = QSpinBox()
        self.address_spin.setRange(1, 99)
        self.address_spin.setValue(self.parent.config[self.key]["address"])
        self.confirm_button = QPushButton(self.parent.translator.translate("confirm"))
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(QLabel(self.parent.translator.translate("only_one_pirani")))
        layout.addWidget(QLabel(self.parent.translator.translate("enter_new_address")))
        layout.addWidget(self.address_spin)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

    def confirm(self):
        self.parent.config[self.key]["address"] = self.address_spin.value()
        self.parent.config.save_config()
        self.close()

class PiraniConfig(QWidget):
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key
        super(PiraniConfig, self).__init__(None)

        self.setWindowTitle(self.parent.translator.translate("pirani_config"))

        # Layout
        layout = QGridLayout()

        # Set node address
        self.node_address_label = QLabel(self.parent.translator.translate("node_address"))
        self.node_address_button = QPushButton(self.parent.translator.translate("set_node_address"))
        self.node_address_button.clicked.connect(self.set_node_address)
        layout.addWidget(self.node_address_label, 0, 0)
        layout.addWidget(self.node_address_button, 0, 1)

        # Setpoint high
        self.setpoint_high_spin = QDoubleSpinBox()
        self.setpoint_high_spin.setRange(0, 1000)
        self.setpoint_high_spin.setValue(self.parent.config[self.key]["setpoint_high"])
        self.setpoint_high_unit = QLabel("unit")
        layout.addWidget(QLabel(self.parent.translator.translate("setpoint_high")), 1, 0)
        layout.addWidget(self.setpoint_high_spin, 1, 1)
        layout.addWidget(self.setpoint_high_unit, 1, 2)

        # Setpoint low
        self.setpoint_low_spin = QDoubleSpinBox()
        self.setpoint_low_spin.setRange(0, 1000)
        self.setpoint_low_spin.setValue(self.parent.config[self.key]["setpoint_low"])
        self.setpoint_low_unit = QLabel("unit")
        layout.addWidget(QLabel(self.parent.translator.translate("setpoint_low")), 2, 0)
        layout.addWidget(self.setpoint_low_spin, 2, 1)
        layout.addWidget(self.setpoint_low_unit, 2, 2)

        # Gas type
        self.gas_type_combo = QComboBox()
        self.gas_type_combo.addItems(["N2", "O2", "Ar", "He"])  # Add your gas types here
        self.gas_type_combo.setCurrentText(self.parent.config[self.key]["gas_type"])
        layout.addWidget(QLabel(self.parent.translator.translate("gas_type")), 3, 0)
        layout.addWidget(self.gas_type_combo, 3, 1)

        # Pressure unit
        self.pressure_unit_combo = QComboBox()
        self.pressure_unit_combo.addItems(["Torr", "Pascal", "mBar"])  # Add your pressure units here
        self.pressure_unit_combo.setCurrentText(self.parent.config[self.key]["pressure_unit"])
        self.pressure_unit_combo.currentIndexChanged.connect(self.update_units)
        layout.addWidget(QLabel(self.parent.translator.translate("pressure_unit")), 4, 0)
        layout.addWidget(self.pressure_unit_combo, 4, 1)

        # Calibrate gauge
        self.calibrate_button = QPushButton(self.parent.translator.translate("calibrate_gauge"))
        layout.addWidget(self.calibrate_button, 5, 0, 1, 2)

        # Gauge status bits
        self.status_bits_label = QLabel(self.parent.translator.translate("gauge_status_bits"))
        layout.addWidget(self.status_bits_label, 6, 0, 1, 2)

        # Gauge SN
        self.sn_label = QLabel(self.parent.translator.translate("gauge_sn"))
        layout.addWidget(self.sn_label, 7, 0, 1, 2)

        # Confirm button
        self.confirm_button = QPushButton(self.parent.translator.translate("confirm"))
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button, 8, 0, 1, 2)

        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())  # Limit the window size to the size hint

        self.current_unit = self.parent.config[self.key]["pressure_unit"]
        self.conversion_factors = {"Torr": 1, "Pascal": 133.322, "mBar": 1.33322}

        self.update_units()

    def confirm(self):
        self.parent.config[self.key]["setpoint_high"] = self.setpoint_high_spin.value()
        self.parent.config[self.key]["setpoint_low"] = self.setpoint_low_spin.value()
        self.parent.config[self.key]["gas_type"] = self.gas_type_combo.currentText()
        self.parent.config[self.key]["pressure_unit"] = self.pressure_unit_combo.currentText()
        self.parent.config.save_config()
        self.close()

    def update_units(self):
        new_unit = self.pressure_unit_combo.currentText()
        self.setpoint_high_unit.setText(new_unit)
        self.setpoint_low_unit.setText(new_unit)

        conversion_factor = self.conversion_factors[new_unit] / self.conversion_factors[self.current_unit]

        self.setpoint_high_spin.setValue(self.setpoint_high_spin.value() * conversion_factor)
        self.setpoint_low_spin.setValue(self.setpoint_low_spin.value() * conversion_factor)

        self.current_unit = new_unit

    def set_node_address(self):
        self.node_address_window = NodeAddressWindow(self.parent, self.key)
        self.node_address_window.show()
