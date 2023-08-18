from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer,QThread, pyqtSignal
from internal.constant import Cmd

from PyQt5.QtCore import QPropertyAnimation, QPoint

class ThrottleValveThread(QThread):
    class StopThreadException(Exception):
        pass

    stepUpdated = pyqtSignal(str, int, int)
    finishedCycle = pyqtSignal()
    targetPressure = 40
    
    def __init__(self, parent, selected_steps, repetitions):
        super().__init__()

        self.parent = parent
        self.main_parent = parent.parent

        self.serial_reader = self.main_parent.serial_reader
        self.config = self.main_parent.config
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
                    self.sleep_while_running(1)
                self.sleep_while_running(1)
        except self.StopThreadException:
            pass
        self.finishedCycle.emit()


    def set_position(self, value):
        while self.serial_reader.busy == True:
            self.sleep_while_running(1)
        self.serial_reader.busy = True # tell to serial_reader that it will be busy for some time
        self.parent.set_position(value)
        self.serial_reader.busy = False # free the serial reader

    def move_position_and_wait(self,position):
        self.set_position(position)
        while(self.parent.step != position):
            self.sleep_while_running(0.5)



    def sleep_while_running(self, seconds):
        milliseconds = int(seconds * 1000)
        for _ in range(milliseconds // 100):
            if not self.is_running:
                raise self.StopThreadException()
            self.msleep(100)

    def read_pressure(self):
        return self.main_parent.custom_widgets["chamber_pressure"].get_value()


    def wait_pressure_or_time(self,pressure,time):
        """
        Attendre que la pression soit atteinte ou que le temps soit écoulé

        Args:
            pressure (float): Pression à atteindre
            time (int): Temps à attendre en secondes
        """
        while self.read_pressure() < pressure and time > 0:
            self.sleep_while_running(1)
            time -= 1

    def return_to_close(self):
        self.set_position(800)  # Retourner à 800
        self.sleep_while_running(self.config.get_constant_value("close_time_at_800"))


    def start_close_calibration(self):
        self.lower_bound = 0
        self.upper_bound = 600

        self.return_to_close()

        self.current_value = int((self.lower_bound + self.upper_bound) / 2)
        self.set_position(self.current_value)
        self.wait_pressure_or_time(self.targetPressure, self.config.get_constant_value("close_time_max_pressure"))  # Attendre que la pression soit atteinte ou que le temps soit écoulé

        self.return_to_close()

    def calibrate_close_position(self):
        self.start_close_calibration()

        while self.upper_bound - self.lower_bound > 1 and self.is_running:
            pressure = self.read_pressure()

            if pressure > self.targetPressure:
                self.lower_bound = self.current_value
            else:
                self.upper_bound = self.current_value

            self.current_value = int((self.lower_bound + self.upper_bound) / 2)
            self.set_position(self.current_value)  # Régler la valeur de dichotomie suivante
            self.wait_pressure_or_time(self.targetPressure, self.config.get_constant_value("close_time_max_pressure"))  # Attendre que la pression soit atteinte ou que le temps soit écoulé

            self.return_to_close()
            self.sleep_while_running(self.config.get_constant_value("close_time_at_800"))

        if(self.lower_bound != self.test):
            print('Close position: ', self.lower_bound)



    def home(self):
        self.move_position_and_wait(200)

        self.set_position(-100) # -1 = home

        self.sleep_while_running(5)


    def open_close(self):
        self.set_position(800)
        self.sleep_while_running(15)
        self.set_position(0)
        self.sleep_while_running(15)






class ThrottleValveGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Throttle Valve GUI')

        self.parent = parent
        self.main_parent = parent.parent
        self.serial_reader = self.main_parent.serial_reader

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

        self.setWindowIcon(self.main_parent.icon)

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
        self.throttle_valve_thread = ThrottleValveThread(self.parent, selected_steps, repetitions)
        self.throttle_valve_thread.stepUpdated.connect(self.update_step_labels)
        self.throttle_valve_thread.finishedCycle.connect(self.on_finished_cycle)
        self.throttle_valve_thread.start()

    def stop_actions(self):
        if hasattr(self, 'throttle_valve_thread'):
            self.throttle_valve_thread.is_running = False
            self.throttle_valve_thread.quit()
            self.throttle_valve_thread.wait()

    def update_step_labels(self, step_name, sub_step, total_repetitions):
        self.step_label.setText(f'Étape: {step_name}')
        self.sub_step_label.setText(f'Sous-étape: {sub_step}/{total_repetitions}')

    def on_finished_cycle(self):
        self.start_stop_button.setText('Start')
        self.stop_actions()


    def closeEvent(self, event):
        self.stop_actions()
        event.accept()
        self.close()

