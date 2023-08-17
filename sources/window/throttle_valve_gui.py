from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer,QThread, pyqtSignal




class ThrottleValveThread(QThread):
    class StopThreadException(Exception):
        pass

    stepUpdated = pyqtSignal(str, int, int)
    finishedCycle = pyqtSignal()
    targetPressure = 40
    
    def __init__(self, serial_reader, selected_steps, repetitions):
        super().__init__()
        self.serial_reader = serial_reader
        self.steps = selected_steps
        self.repetitions = repetitions
        self.is_running = True

        self.test = 447

    def run(self):
        try:
            for step_index, step_name in enumerate(self.steps):
                for sub_step in range(self.repetitions[step_index]):
                    self.test += 1
                    self.stepUpdated.emit(step_name, sub_step + 1, self.repetitions[step_index])
                    getattr(self, step_name.replace(' ', '_'))()
                    self.sleep_while_running(1000)
                self.sleep_while_running(1000)
        except self.StopThreadException:
            pass
        self.finishedCycle.emit()


    def set_value(self, value):
        while self.serial_reader.busy == True:
            print("t")
            self.sleep_while_running(1000)

        self.serial_reader.busy = True # tell to serial_reader that it will be busy for some time
        # self.parent.serial_reader.send_data(1,self.parent.cmd.Port)
        # data = self.parent.serial_reader.wait_and_read_data(1)
        self.serial_reader.busy = False # free the serial reade


    def sleep_while_running(self, milliseconds):
        for _ in range(milliseconds // 100):
            if not self.is_running:
                raise self.StopThreadException()
            self.msleep(100)

    def read_pressure(self):
        return (self.current_value-self.test+40)


    def wait_pressure_or_time(self,pressure,time):
        """
        Attendre que la pression soit atteinte ou que le temps soit écoulé

        Args:
            pressure (float): Pression à atteindre
            time (int): Temps à attendre en secondes
        """
        while self.read_pressure() < pressure and time > 0:
            self.sleep_while_running(1000)
            time -= 1

    def calibrate_close_position(self):
        print('Calibrate close position')
        self.lower_bound = 150
        self.upper_bound = 450
        self.current_value = int((self.lower_bound + self.upper_bound) / 2)
        self.set_value(self.current_value)
        self.wait_pressure_or_time(self.targetPressure, 25)  # Attendre que la pression soit atteinte ou que le temps soit écoulé


        while self.upper_bound - self.lower_bound > 1 and self.is_running:
            pressure = self.read_pressure()


            if pressure <= self.targetPressure:
                self.lower_bound = self.current_value
            else:
                self.upper_bound = self.current_value

            self.current_value = int((self.lower_bound + self.upper_bound) / 2)
            self.set_value(self.current_value)  # Régler la valeur de dichotomie suivante
            self.wait_pressure_or_time(self.targetPressure, 25)  # Attendre que la pression soit atteinte ou que le temps soit écoulé

            self.set_value(800)  # Retourner à 800
            self.sleep_while_running(15000)

        if(self.lower_bound != self.test):
            print('lower bound: ', self.lower_bound)
            print('upper bound: ', self.upper_bound)
            print('test: ', self.test)


    def home(self):
        self.set_value(200)
        self.sleep_while_running(1000)





class ThrottleValveGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Throttle Valve GUI')
        
        self.parent = parent
        self.serial_reader = parent.serial_reader

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


        self.setLayout(layout)


    def start_stop(self):
        if self.start_stop_button.text() == 'Start':
            self.start_stop_button.setText('Stop')
            self.start_actions()
        else:
            self.start_stop_button.setText('Start')
            self.stop_actions()

    def start_actions(self):
        selected_steps = []
        repetitions = []
        for step, (checkbox, spinbox) in zip(self.steps, self.step_spinboxes):
            if checkbox.isChecked():
                selected_steps.append(step)
                repetitions.append(spinbox.value())
        self.throttle_valve_thread = ThrottleValveThread(self.serial_reader, selected_steps, repetitions)
        self.throttle_valve_thread.stepUpdated.connect(self.update_step_labels)
        self.throttle_valve_thread.finishedCycle.connect(self.on_finished_cycle)
        self.throttle_valve_thread.start()

    def stop_actions(self):
        if hasattr(self, 'throttle_valve_thread'):
            print('Stopping thread')
            self.throttle_valve_thread.is_running = False
            self.throttle_valve_thread.quit()
            self.throttle_valve_thread.wait()
            print('Thread stopped') 

    def update_step_labels(self, step_name, sub_step, total_repetitions):
        self.step_label.setText(f'Étape: {step_name}')
        self.sub_step_label.setText(f'Sous-étape: {sub_step}/{total_repetitions}')

    def on_finished_cycle(self):
        self.start_stop_button.setText('Start')
        self.stop_actions()


    def closeEvent(self, event):
        self.stop_actions()
        event.accept()