from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QDate, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from internal.logger import Logger

import csv
import os

class ThrottleValveThread(QThread):
    class StopThreadException(Exception):
        pass

    stepUpdated = pyqtSignal(str, int, int)
    finishedCycle = pyqtSignal()
    
    def __init__(self, parent, selected_steps, repetitions):
        super().__init__()

        self.gui = parent
        self.parent = parent.parent
        self.main_parent = parent.parent.parent
        self.translator = self.main_parent.translator

        self.serial_reader = self.main_parent.serial_reader
        self.config = self.main_parent.config
        self.steps = selected_steps
        self.repetitions = repetitions
        self.is_running = True
        
        self.targetPressure = self.config.get_constant_value("close_ref")

    def run(self):
        try:
            for step_index, step_name in enumerate(self.steps):
                self.y_values = []
                for sub_step in range(self.repetitions[step_index]):
                    self.stepUpdated.emit(step_name, sub_step + 1, self.repetitions[step_index])
                    getattr(self, step_name.replace(" ", "_"))()
                    self.sleep_while_running(1)
                # Sauvegarder les valeurs dans un fichier CSV
                self.save_to_csv(self.y_values,step_name)
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
            self.sleep_while_running(0.2)



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

    def calibrate_hysteresis(self):
        Logger.error("Calibration de l'hystérésis non implémentée")


    def return_to_close(self):
        self.set_position(800)  # Retourner à 800
        self.sleep_while_running(self.config.get_constant_value("close_time_at_800"))


    def calibrate_close_position(self):
        self.lower_bound = 0
        self.upper_bound = 600
        print("t")
        self.return_to_close()

        # while self.upper_bound - self.lower_bound > 1 and self.is_running:
            # self.current_value = int((self.lower_bound + self.upper_bound) / 2)
            # self.set_position(self.current_value)  # Régler la valeur de dichotomie suivante
            # self.wait_pressure_or_time(self.targetPressure, self.config.get_constant_value("close_time_max_pressure"))  # Attendre que la pression soit atteinte ou que le temps soit écoulé
            
            # self.sleep_while_running(1)

            # pressure = self.read_pressure()
            # print(pressure)
            # print(self.targetPressure)
            # if pressure > self.targetPressure:
            #     self.lower_bound = self.current_value
            # else:
            #     self.upper_bound = self.current_value


            # self.return_to_close()
            
        # Ajouter la valeur de lower_bound à y_values
        self.y_values.append(self.upper_bound)

        # Mettre à jour le graphique avec un titre
        self.gui.update_graph(self.y_values, "Calibration de la position fermée")




    def home(self):
        self.parent.home()

        self.sleep_while_running(5)


    def open_close(self):
        self.parent.open()
        self.move_position_and_wait(800)
        self.sleep_while_running(2)
        self.parent.close()
        self.move_position_and_wait(0)
        self.sleep_while_running(2)



    def get_home_value(self):
        # Fonction vierge pour obtenir la valeur de Home
        return 0

    def get_open_close_value(self):
        # Fonction vierge pour obtenir la valeur de open_close
        return 0

    def get_hysteresis_value(self):
        # Fonction vierge pour obtenir la valeur de hysteresis
        return 0

    def save_to_csv(self, y_values,step_name):

        filename = self.gui.filename
        path = f"data/throttle_valve/{filename}/{step_name}.csv"

        #create data folder if it doesn't exist
        os.makedirs("data",exist_ok= True)
        os.makedirs(f"data/throttle_valve",exist_ok= True)
        os.makedirs(f"data/throttle_valve/{filename}",exist_ok= True)

        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["cycle", "value"])

            for i, value in enumerate(y_values):
                writer.writerow([i, value])



class ThrottleValveGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.main_parent = parent.parent
        self.translator = self.main_parent.translator
        self.serial_reader = self.main_parent.serial_reader
        self.filename = ""
        self.state = 0

        self.setWindowTitle(self.translator.translate("throttle_valve_gui_title"))

        # Layout principal
        layout = QtWidgets.QGridLayout()

        # Layout gauche pour les contrôles existants
        left_layout = QtWidgets.QVBoxLayout()


        # Choix des étapes
        self.steps = ["home", "open_close","calibrate_hysteresis","calibrate_close_position"]
        self.step_spinboxes = []

        step_layout = QtWidgets.QGridLayout()

        nb_cycle_label = QtWidgets.QLabel(self.translator.translate("cycles"),alignment=Qt.AlignmentFlag.AlignHCenter)
        name_label = QtWidgets.QLabel(self.translator.translate("name_label"),alignment=Qt.AlignmentFlag.AlignHCenter)
        step_layout.addWidget(nb_cycle_label, 0, 0)
        step_layout.addWidget(name_label, 0, 1)

        for index, step in enumerate(self.steps):
            checkbox = QtWidgets.QCheckBox(self.translator.translate(step))
            spinbox = QtWidgets.QSpinBox()
            step_layout.addWidget(spinbox, index+1, 0)
            step_layout.addWidget(checkbox, index+1, 1)
            self.step_spinboxes.append((checkbox, spinbox))

        left_layout.addLayout(step_layout)

        # Ajouter un espace
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        left_layout.addItem(spacer)

        # Zone pour PN et SN
        pn_layout = QtWidgets.QHBoxLayout()
        pn_label = QtWidgets.QLabel(self.translator.translate("pn_label"))
        self.pn_text = QtWidgets.QLineEdit()
        self.pn_text.textChanged.connect(self.update_csv_file)
        pn_layout.addWidget(pn_label)
        pn_layout.addWidget(self.pn_text)
        left_layout.addLayout(pn_layout)

        sn_layout = QtWidgets.QHBoxLayout()
        sn_label = QtWidgets.QLabel(self.translator.translate("sn_label"))
        self.sn_text = QtWidgets.QLineEdit()
        self.sn_text.textChanged.connect(self.update_csv_file)
        sn_layout.addWidget(sn_label)
        sn_layout.addWidget(self.sn_text)
        left_layout.addLayout(sn_layout)

        # Ajouter un espace
        left_layout.addItem(spacer)

        # Bouton start/stop
        self.start_stop_button = QtWidgets.QPushButton(self.translator.translate("start_button"))
        self.start_stop_button.setEnabled(False)
        self.start_stop_button.clicked.connect(self.start_stop)
        left_layout.addWidget(self.start_stop_button)

        # Affichage de l"étape et de la sous-étape
        self.step_label = QtWidgets.QLabel(self.translator.translate("step_label", step=0))
        self.sub_step_label = QtWidgets.QLabel(self.translator.translate("sub_step_label", sub_step=0))
        left_layout.addWidget(self.step_label)
        left_layout.addWidget(self.sub_step_label)

        # Ajouter le layout gauche à la première colonne du layout principal
        layout.addLayout(left_layout, 0, 0)

        # Layout droit pour le graphique
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Ajouter le canvas à la deuxième colonne du layout principal
        layout.addWidget(self.canvas, 0, 1)

        self.setLayout(layout)
        self.setWindowIcon(self.main_parent.icon)


    def start_stop(self):
        if self.state == 0:
            self.state = 1
            self.start_stop_button.setText(self.translator.translate("stop_button"))
            self.start_actions()
        else:
            self.state = 0
            self.start_stop_button.setText(self.translator.translate("start_button"))
            self.stop_actions()

    def start_actions(self):
        selected_steps = []
        repetitions = []
        for step, (checkbox, spinbox) in zip(self.steps, self.step_spinboxes):
            if checkbox.isChecked():
                selected_steps.append(step)
                repetitions.append(spinbox.value())
        self.throttle_valve_thread = ThrottleValveThread(self, selected_steps, repetitions)
        self.throttle_valve_thread.stepUpdated.connect(self.update_step_labels)
        self.throttle_valve_thread.finishedCycle.connect(self.on_finished_cycle)
        self.throttle_valve_thread.start()

    def stop_actions(self):
        if hasattr(self, "throttle_valve_thread"):
            self.throttle_valve_thread.is_running = False
            self.throttle_valve_thread.quit()
            self.throttle_valve_thread.wait()

    def update_csv_file(self):
        """
        Met à jour le nom du fichier CSV en fonction des entrées PN et SN.
        """
        pn = self.pn_text.text()
        sn = self.sn_text.text()
        if pn and sn:
            date = QDate.currentDate().toString("yyyy-MM-dd")
            filename = f"{pn}-{sn}-{date}"
            self.filename = filename  # Sauvegarde du nom de fichier dans l'attribut de la classe
            self.start_stop_button.setEnabled(True)  # Active le bouton start/stop si PN et SN sont définis
        else:
            self.filename = ""  # Réinitialise le nom de fichier si PN ou SN sont vides
            self.start_stop_button.setEnabled(False)  # Désactive le bouton start/stop si PN ou SN sont vides

    def update_step_labels(self, step_name, sub_step, total_repetitions):
        self.step_label.setText(self.translator.translate("step_label", step=step_name))
        self.sub_step_label.setText(self.translator.translate("sub_step_label", sub_step=f"{sub_step}/{total_repetitions}"))

    def on_finished_cycle(self):
        self.start_stop_button.setText(self.translator.translate("start_button"))
        self.stop_actions()

    def update_graph(self, y_values, title):
        self.ax.clear()
        x_values = range(len(y_values))
        self.ax.plot(x_values, y_values)
        self.ax.set_title(self.translator.translate(title))
        self.canvas.draw()


    def closeEvent(self, event):
        self.stop_actions()
        event.accept()
        self.close()

