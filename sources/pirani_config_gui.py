from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QGridLayout, QDoubleSpinBox, QMessageBox, QSpinBox)

from internal.constant import PiraniConfig

class NodeAddressWindow(QWidget):
    def __init__(self, parent):
        self.parent = parent #windows PiraniConfigGui

        self.key = parent.key
        self.main_parent = parent.parent #main objet (gui)
        super(NodeAddressWindow, self).__init__(None)
        self.setWindowTitle(self.main_parent.translator.translate("set_node_address"))

        layout = QVBoxLayout()
        self.address_spin = QSpinBox()
        self.address_spin.setRange(1, 99)
        self.address_spin.setValue(self.main_parent.config[self.key]["address"])
        self.confirm_button = QPushButton(self.main_parent.translator.translate("confirm"))
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(QLabel(self.main_parent.translator.translate("enter_new_address")))
        layout.addWidget(self.address_spin)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

        self.setWindowIcon(self.main_parent.icon)

    def confirm(self):
        self.main_parent.config[self.key]["address"] = self.address_spin.value()
        self.main_parent.RS485.pirani[self.key].update_address()
        self.main_parent.config.save_config()
        self.parent.update_node_address_label()
        self.close()

class PiraniConfigGui(QWidget):
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key
        super(PiraniConfigGui, self).__init__(None)

        self.setWindowTitle(self.parent.translator.translate("pirani_config"))
        self.setWindowIcon(self.parent.icon)

        # Layout
        layout = QGridLayout()

        # Set node address
        self.node_address_label = QLabel()
        self.update_node_address_label()
        self.node_address_button = QPushButton(self.parent.translator.translate("set_node_address"))
        self.node_address_button.clicked.connect(self.set_node_address)
        layout.addWidget(self.node_address_label, 0, 0)
        layout.addWidget(self.node_address_button, 0, 1)

        # Setpoint high
        self.setpoint_high_spin = QDoubleSpinBox()
        self.setpoint_high_spin.setMaximum(100000)
        self.setpoint_high_spin.setValue(self.parent.config[self.key]["setpoint_high"])
        self.setpoint_high_unit = QLabel("unit")
        self.setpoint_high_unit.setMaximumWidth(60)

        layout.addWidget(QLabel(self.parent.translator.translate("setpoint_high")), 1, 0)
        layout.addWidget(self.setpoint_high_spin, 1, 1)
        layout.addWidget(self.setpoint_high_unit, 1, 2)

        # Setpoint low
        self.setpoint_low_spin = QDoubleSpinBox()
        self.setpoint_low_spin.setMaximum(100000)
        self.setpoint_low_spin.setValue(self.parent.config[self.key]["setpoint_low"])
        self.setpoint_low_unit = QLabel("unit")
        self.setpoint_low_unit.setMaximumWidth(60)
        layout.addWidget(QLabel(self.parent.translator.translate("setpoint_low")), 2, 0)
        layout.addWidget(self.setpoint_low_spin, 2, 1)
        layout.addWidget(self.setpoint_low_unit, 2, 2)

        # Gas type
        self.gas_type_combo = QComboBox()
        self.gas_type_combo.addItems(PiraniConfig.gas_types)
        self.gas_type_combo.setCurrentText(self.parent.config[self.key]["gas_type"])
        layout.addWidget(QLabel(self.parent.translator.translate("gas_type",gas_type="")), 3, 0)
        layout.addWidget(self.gas_type_combo, 3, 1)

        # Pressure unit
        self.pressure_unit_combo = QComboBox()
        self.pressure_unit_combo.addItems(PiraniConfig.units_types)  # Add your pressure units here
        self.pressure_unit_combo.setCurrentText(self.parent.config[self.key]["pressure_unit"])
        self.pressure_unit_combo.currentIndexChanged.connect(self.update_units)
        layout.addWidget(QLabel(self.parent.translator.translate("pressure_unit")), 4, 0)
        layout.addWidget(self.pressure_unit_combo, 4, 1)

        # Calibrate gauge
        self.calibrate_button = QPushButton(self.parent.translator.translate("calibrate_gauge"))
        self.calibrate_button.clicked.connect(self.calibrate_gauge)
        layout.addWidget(self.calibrate_button, 5, 0, 1, 2)


        # Gauge status bits
        self.status_bits_label = QLabel(self.parent.translator.translate("gauge_status_bits"))
        self.status_bits_value = QLabel("0000 0000 0000 0000")  # initial value
        layout.addWidget(self.status_bits_label, 6, 0)
        layout.addWidget(self.status_bits_value, 6, 1)  # add this to the layout

        # Gauge SN
        self.sn_label = QLabel(self.parent.translator.translate("gauge_sn"))
        self.sn_value = QLabel(self.parent.RS485.pirani[self.key].read_SN())  # replace "SN Value" with the actual initial value
        layout.addWidget(self.sn_label, 7, 0)
        layout.addWidget(self.sn_value, 7, 1)  # add this to the layout


        # Confirm button
        self.confirm_button = QPushButton(self.parent.translator.translate("confirm"))
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button, 8, 0, 1, 2)

        layout.setColumnMinimumWidth(1,180)
        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())  # Limit the window size to the size hint

        self.current_unit = self.parent.config[self.key]["pressure_unit"]
        self.conversion_factors = {"Torr": 1, "Pascal": 133.322, "mBar": 1.33322}

        self.update_units()

    def confirm(self):
        config = self.parent.config[self.key]
        config["setpoint_high"] = self.setpoint_high_spin.value()
        config["setpoint_low"] = self.setpoint_low_spin.value()
        config["gas_type"] = self.gas_type_combo.currentText()
        config["pressure_unit"] = self.pressure_unit_combo.currentText()
        self.parent.RS485.pirani[self.key].update_config()
        self.parent.config.save_config()
        self.close()
        self = None

    def update_units(self):
        new_unit = self.pressure_unit_combo.currentText()
        self.setpoint_high_unit.setText(new_unit)
        self.setpoint_low_unit.setText(new_unit)

        conversion_factor = self.conversion_factors[new_unit] / self.conversion_factors[self.current_unit]


        setpoint_high = self.setpoint_high_spin.value() * conversion_factor
        setpoint_low = self.setpoint_low_spin.value() * conversion_factor

        # Update the maximum values for the setpoint spin boxes
        max_value = 851 * self.conversion_factors[new_unit]
        self.setpoint_high_spin.setMaximum(max_value)
        self.setpoint_low_spin.setMaximum(max_value)

        self.setpoint_high_spin.setValue(setpoint_high)
        self.setpoint_low_spin.setValue(setpoint_low)

        self.current_unit = new_unit

    def update_status_bits(self, status_bits):
        # Convert status_bits to binary and format it with spaces
        binary_status_bits = format(status_bits, '016b')
        formatted_status_bits = ' '.join(binary_status_bits[i:i+4] for i in range(0, len(binary_status_bits), 4))
        self.status_bits_value.setText(formatted_status_bits)


    def set_node_address(self):
        QMessageBox.warning(self, self.parent.translator.translate("warning"), self.parent.translator.translate("only_one_pirani"))
        self.node_address_window = NodeAddressWindow(self)
        self.node_address_window.show()

    def update_node_address_label(self):
        self.node_address_label.setText(self.parent.translator.translate("node_address", value=self.parent.config[self.key]["address"]))

    
    def calibrate_gauge(self):
        self.parent.RS485.pirani[self.key].calibrate()