from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

class ThrottleValveGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Throttle Valve GUI')

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Zone pour PN et SN
        pn_layout = QtWidgets.QHBoxLayout()
        pn_label = QtWidgets.QLabel('PN:')
        self.pn_text = QtWidgets.QLineEdit()
        pn_layout.addWidget(pn_label)
        pn_layout.addWidget(self.pn_text)
        layout.addLayout(pn_layout)

        sn_layout = QtWidgets.QHBoxLayout()
        sn_label = QtWidgets.QLabel('SN:')
        self.sn_text = QtWidgets.QLineEdit()
        sn_layout.addWidget(sn_label)
        sn_layout.addWidget(self.sn_text)
        layout.addLayout(sn_layout)

        # Choix des étapes
        self.steps = ['home', 'open_close', 'calibrate_hysteresis', 'calibrate_close_position']
        self.step_spinboxes = []
        for step in self.steps:
            step_layout = QtWidgets.QHBoxLayout()
            checkbox = QtWidgets.QCheckBox(step)
            spinbox = QtWidgets.QSpinBox()
            step_layout.addWidget(checkbox)
            step_layout.addWidget(spinbox)
            layout.addLayout(step_layout)
            self.step_spinboxes.append((checkbox, spinbox))

        # Bouton start/stop
        self.start_stop_button = QtWidgets.QPushButton('Start')
        self.start_stop_button.clicked.connect(self.start_stop)
        layout.addWidget(self.start_stop_button)

        # Affichage de l'étape et de la sous-étape
        self.step_label = QtWidgets.QLabel('Étape: 0')
        self.sub_step_label = QtWidgets.QLabel('Sous-étape: 0')
        layout.addWidget(self.step_label)
        layout.addWidget(self.sub_step_label)

        # QTimer pour vérifier les capteurs
        self.sensor_timer = QTimer()
        self.sensor_timer.timeout.connect(self.check_sensors)
        self.sensor_timer.setInterval(40)  # Vérifier les capteurs toutes les 40 ms

        # Variables pour la dichotomie
        self.target_pressure = 40
        self.check_pressure_timer = QTimer()
        self.check_pressure_timer.setInterval(1000)  # 1 seconde en ms
        self.check_pressure_timer.timeout.connect(self.check_pressure)

        # QTimer pour commencer à vérifier la pression après 15 secondes
        self.timeout_timer = QTimer()
        self.timeout_timer.setInterval(15 * 1000)  # 15 secondes en ms
        self.timeout_timer.timeout.connect(self.start_checking_pressure)

        # QTimer pour lancer la dichotomie après 25 secondes
        self.dichotomy_timer = QTimer()
        self.dichotomy_timer.setInterval(25 * 1000)  # 25 secondes en ms
        self.dichotomy_timer.timeout.connect(self.dichotomy_step)
        self.dichotomy_timer.setSingleShot(True)  # S'exécute une seule fois


        self.setLayout(layout)


    def start_stop(self):
        if self.start_stop_button.text() == 'Start':
            self.start_stop_button.setText('Stop')
            self.start_actions()
        else:
            self.start_stop_button.setText('Start')
            self.stop_actions()

    def start_actions(self):
        self.current_step = 0
        self.current_sub_step = 0
        self.execute_step()

    def stop_actions(self):
        self.check_pressure_timer.stop()
        self.sensor_timer.stop()
        self.timeout_timer.stop()
        self.dichotomy_timer.stop()  # Arrêter le délai d'attente de 25 secondes

    def execute_step(self):
        if self.current_step < len(self.step_spinboxes):
            checkbox, spinbox = self.step_spinboxes[self.current_step]
            if checkbox.isChecked():
                step_name = self.steps[self.current_step]
                self.current_repetitions = spinbox.value()
                if self.current_sub_step < self.current_repetitions:
                    self.step_label.setText(f'Étape: {step_name}')
                    self.sub_step_label.setText(f'Sous-étape: {self.current_sub_step + 1}/{self.current_repetitions}')
                    getattr(self, step_name.replace(' ', '_'))()  # Appel de la fonction correspondante
                    return
                else:
                    self.current_sub_step = 0
            self.current_step += 1
            self.execute_step()
        else:
            self.start_stop_button.setText('Start')
            self.stop_actions()

    def calibrate_close_position(self):
        print('Calibrate close position')
        self.lower_bound = 150
        self.upper_bound = 450
        self.current_value = int((self.lower_bound + self.upper_bound) / 2)
        self.set_value(self.current_value)
        self.sensor_timer.start()  # Commencer à vérifier les capteurs
        self.dichotomy_timer.start()  # Commencer le délai d'attente de 25 secondes

    def start_checking_pressure(self):
        self.timeout_timer.stop()  # Arrêter le délai d'attente de 15 secondes
        self.current_value = int((self.lower_bound + self.upper_bound) / 2)
        self.set_value(self.current_value)  # Régler la valeur de dichotomie suivante
        self.check_pressure_timer.start()  # Commencer à vérifier la pression toutes les secondes

        if self.upper_bound - self.lower_bound <= 1:
            self.stop_actions()
            self.current_sub_step += 1
            self.execute_step()
        else:
            self.dichotomy_timer.start()  # Recommencer le délai d'attente de 25 secondes

    def dichotomy_step(self):
        self.check_pressure_timer.stop()  # Arrêter de vérifier la pression toutes les secondes
        self.dichotomy_timer.stop()  # Arrêter le délai d'attente de 25 secondes

        pressure = self.read_pressure()
        print("current value: ", self.current_value)
        print("fake pressure: ", pressure)

        if pressure < self.target_pressure:
            self.lower_bound = self.current_value
        else:
            self.upper_bound = self.current_value

        self.set_value(800)  # Retourner à 800
        self.timeout_timer.start()  # Commencer le délai d'attente de 15 secondes

    def check_pressure(self):
        pressure = self.read_pressure()
        print(pressure)
        if pressure >= self.target_pressure:
            self.dichotomy_timer.stop()  # Arrêter le délai d'attente de 25 secondes
            self.dichotomy_step()


    def check_sensors(self):
        # Lire les capteurs ici
        pass

    def set_value(self, value):
        # Code pour régler la valeur
        print("set value: ", value)
        pass

    def read_pressure(self):

        return (self.current_value-174+40)


    # Autres méthodes pour les autres étapes ici

    def closeEvent(self, event):
        self.stop_actions()
        event.accept()