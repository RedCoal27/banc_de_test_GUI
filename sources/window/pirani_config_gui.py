"""
This module contains two classes: NodeAddressWindow and PiraniConfigGui.

NodeAddressWindow is a QWidget that allows the user to set a new address for a Pirani gauge.

PiraniConfigGui is a QWidget that allows the user to configure various settings for a Pirani gauge, such as setpoint high and low, gas type, pressure unit, and gauge status bits.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QComboBox, QGridLayout, QDoubleSpinBox, QMessageBox, QSpinBox, QToolButton, QMenu, QAction)

from internal.constant import PiraniConfig



class NodeAddressWindow(QWidget):
    """
    Une classe représentant une fenêtre pour définir l'adresse du nœud.

    Attributes:
        parent: la fenêtre parent (PiraniConfigGui)
        key: la clé pour le dictionnaire de configuration
        main_parent: l'objet principal (gui)
        address_spin: un QSpinBox pour entrer la nouvelle adresse
        confirm_button: un QPushButton pour confirmer la nouvelle adresse
    """

    def __init__(self, parent):
        """
        Constructeur de la classe NodeAddressWindow.

        Args:
            parent: Objet parent (PiraniConfigGui).
        """
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
        """
        Méthode pour confirmer la nouvelle adresse.

        Cette méthode met à jour le dictionnaire de configuration avec la nouvelle adresse,
        met à jour l'étiquette d'adresse du nœud dans la fenêtre parent, enregistre la configuration,
        et ferme la fenêtre actuelle.
        """
        self.main_parent.config[self.key]["address"] = self.address_spin.value()
        self.main_parent.RS485.pirani[self.key].update_address()
        self.main_parent.config.save_config()
        self.parent.update_node_address_label()
        self.close()

        

class PiraniConfigGui(QWidget):
    """
    Une fenêtre GUI pour la configuration des jauges Pirani.

    Args:
        parent: Le widget parent.
        key: La clé pour la configuration de la jauge.

    Attributes:
        parent: Le widget parent.
        key: La clé pour la configuration de la jauge.
        node_address_label: QLabel pour afficher l'adresse du nœud.
        node_address_button: QPushButton pour définir l'adresse du nœud.
        setpoint_high_spin: QDoubleSpinBox pour définir le point haut.
        setpoint_high_unit: QLabel pour afficher l'unité du point haut.
        setpoint_low_spin: QDoubleSpinBox pour définir le point bas.
        setpoint_low_unit: QLabel pour afficher l'unité du point bas.
        gas_type_combo: QComboBox pour définir le type de gaz.
        pressure_unit_combo: QComboBox pour définir l'unité de pression.
        calibrate_button: QPushButton pour calibrer la jauge.
        status_bits_label: QLabel pour afficher les bits d'état.
        status_bits_button: QPushButton pour afficher les bits d'état.
        status_bits_menu: QMenu pour afficher les bits d'état.
        sn_label: QLabel pour afficher le numéro de série.
        sn_value: QLabel pour afficher la valeur du numéro de série.
        confirm_button: QPushButton pour confirmer la configuration.
        current_unit: L'unité de pression actuelle.
        conversion_factor: Le facteur de conversion actuel.
    """
    def __init__(self, parent, key):
        """
        Constructeur de la classe PiraniConfigGui.

        Args:
            parent: Le widget parent.
            key: La clé pour la configuration de la jauge.
        """
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
        self.status_bits_value.setToolTip(self.parent.translator.translate("status_bits_tooltip"))

        # Create a QToolButton
        self.status_bits_info_button = QToolButton()
        self.status_bits_info_button.setText("?")
        self.status_bits_info_button.setPopupMode(QToolButton.InstantPopup)

        # Create a QMenu
        self.status_bits_info_menu = self.create_status_bits_info_menu(0)  # initial value
        self.status_bits_info_button.setMenu(self.status_bits_info_menu)

        layout.addWidget(self.status_bits_label, 6, 0)
        layout.addWidget(self.status_bits_value, 6, 1)
        layout.addWidget(self.status_bits_info_button, 6, 2)  # add this to the layout


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


    def create_status_bits_info_menu(self, status_bits):
        """
        Crée un menu QMenu pour afficher les informations sur les bits d'état de la jauge.

        Args:
            status_bits: La valeur des bits d'état de la jauge.

        Returns:
            Un QMenu pour afficher les informations sur les bits d'état de la jauge.
        """
        status_bits_info_menu = QMenu(self)

        status_bits_info = [
            {"Bit": self.parent.translator.translate("bit"), "Value": "", "Status Flag": "", "Meaning": self.parent.translator.translate("bit_explanation")},
            {"Bit": "0", "Value": self.get_bit_value(status_bits, 0), "Status Flag": self.parent.translator.translate("gauge_err"), "Meaning": self.parent.translator.translate("gauge_specific_error")},
            {"Bit": "1", "Value": self.get_bit_value(status_bits, 1), "Status Flag": self.parent.translator.translate("mag_n"), "Meaning": self.parent.translator.translate("gauge_magnetron")},
            {"Bit": "2", "Value": self.get_bit_value(status_bits, 2), "Status Flag": self.parent.translator.translate("spop_on"), "Meaning": self.parent.translator.translate("setpoint_status")},
            {"Bit": "3", "Value": self.get_bit_value(status_bits, 3), "Status Flag": self.parent.translator.translate("gauge_lk"), "Meaning": self.parent.translator.translate("gauge_parameters")},
            {"Bit": "4-5", "Value": self.get_multi_bit_value(status_bits, 4, 5), "Status Flag": self.parent.translator.translate("pressure_units"), "Meaning": self.parent.translator.translate("pressure_units_meaning")},
            {"Bit": "6", "Value": self.get_bit_value(status_bits, 6), "Status Flag": self.parent.translator.translate("flashee_err"), "Meaning": self.parent.translator.translate("all_stored_parameters")},
            {"Bit": "7", "Value": self.get_bit_value(status_bits, 7), "Status Flag": self.parent.translator.translate("calibrating"), "Meaning": self.parent.translator.translate("calibration_in_progress")},
            {"Bit": "8", "Value": self.get_bit_value(status_bits, 8), "Status Flag": self.parent.translator.translate("mag_str"), "Meaning": self.parent.translator.translate("memory_striking")},
            {"Bit": "9", "Value": self.get_bit_value(status_bits, 9), "Status Flag": self.parent.translator.translate("mag_strike_fail"), "Meaning": self.parent.translator.translate("magnetron_striking_failure")},
            {"Bit": "10", "Value": self.get_bit_value(status_bits, 10), "Status Flag": self.parent.translator.translate("pir_fil_fail"), "Meaning": self.parent.translator.translate("pirani_filament_failure")},
            {"Bit": "11", "Value": self.get_bit_value(status_bits, 11), "Status Flag": self.parent.translator.translate("str_fil_fail"), "Meaning": self.parent.translator.translate("striker_filament_failure")},
            {"Bit": "12-14", "Value": self.get_multi_bit_value(status_bits, 12, 14), "Status Flag": self.parent.translator.translate("gas_type"), "Meaning": self.parent.translator.translate("gas_type_meaning")},
            {"Bit": "15", "Value": self.get_bit_value(status_bits, 15), "Status Flag": self.parent.translator.translate("mag_exposure"), "Meaning": self.parent.translator.translate("magnetron_exposure_threshold")},
        ]

        for info in status_bits_info:
            if info['Bit'] == self.parent.translator.translate("bit"):
                action_text = f"{info['Meaning']}"
            else:
                action_text = f"{self.parent.translator.translate('bit')}: {info['Bit']}, {self.parent.translator.translate('value')}: {info['Value']}, {self.parent.translator.translate('status_flag')}: {info['Status Flag']}, {self.parent.translator.translate('meaning')}: {info['Meaning']}"
            action = QAction(action_text, self)
            action.setEnabled(False)
            status_bits_info_menu.addAction(action)

        return status_bits_info_menu

    def confirm(self):
        """
        Méthode pour confirmer la configuration de la jauge.

        Cette méthode met à jour la configuration de la jauge, enregistre la configuration,
        et ferme la fenêtre.
        """
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
        """
        Met à jour les unités d'affichage en fonction de l'unité de pression sélectionnée.
        """
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


    def get_bit_value(self, status_bits, bit):
        """
        Obtient la valeur d'un bit donné dans les bits d'état.

        Args:
            status_bits: La valeur des bits d'état.
            bit: Le numéro du bit.

        Returns:
            La valeur du bit (0 ou 1).
        """
        return (status_bits >> bit) & 1

    def get_multi_bit_value(self, status_bits, start_bit, end_bit):
        """
        Obtient la valeur d'un ensemble de bits donné dans les bits d'état.

        Args:
            status_bits: La valeur des bits d'état.
            start_bit: Le numéro du premier bit.
            end_bit: Le numéro du dernier bit.

        Returns:
            La valeur de l'ensemble de bits.
        """
        mask = (2**(end_bit - start_bit + 1) - 1) << start_bit
        return (status_bits & mask) >> start_bit

    def update_status_bits(self, status_bits):
        """
        Met à jour l'affichage des bits d'état.

        Args:
            status_bits: La valeur des bits d'état.
        """
        # Convert status_bits to binary and format it with spaces
        binary_status_bits = format(status_bits, '016b')
        formatted_status_bits = ' '.join(binary_status_bits[i:i+4] for i in range(0, len(binary_status_bits), 4))
        self.status_bits_value.setText(formatted_status_bits)
        # Update the status bits info if the info window is open
        self.status_bits_info_menu = self.create_status_bits_info_menu(status_bits)
        self.status_bits_info_button.setMenu(self.status_bits_info_menu)


    def set_node_address(self):
        """
        Ouvre une fenêtre pour définir l'adresse du nœud.
        """
        QMessageBox.warning(self, self.parent.translator.translate("warning"), self.parent.translator.translate("only_one_pirani"))
        self.node_address_window = NodeAddressWindow(self)
        self.node_address_window.show()

    def update_node_address_label(self):
        """
        Met à jour l'étiquette d'adresse du nœud dans la fenêtre.
        """
        self.node_address_label.setText(self.parent.translator.translate("node_address", value=self.parent.config[self.key]["address"]))

    
    def calibrate_gauge(self):
        """
        Lance la calibration de la jauge.
        """
        self.parent.RS485.pirani[self.key].calibrate()